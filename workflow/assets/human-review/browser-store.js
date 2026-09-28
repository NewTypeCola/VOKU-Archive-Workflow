/* Static adapter for the existing Human Review UI. No review network requests. */
'use strict';
const PublicReview = (() => {
  const STATUSES = ['unreviewed', 'ok', 'issue', 'needs_review'];
  const ISSUES = ['unmasked_name', 'wrong_target', 'mask_geometry', 'text_damage', 'token_missing', 'token_legibility', 'other'];
  const copy = value => structuredClone(value);
  const scope = new URL('.', document.baseURI).pathname;
  let catalog, connection;
  const fail = (message, status = 400) => Object.assign(new Error(message), {status});

  function transaction(stores, mode, work) {
    return new Promise((resolve, reject) => {
      const tx = connection.transaction(stores, mode);
      let result, failure;
      tx.oncomplete = () => resolve(result);
      tx.onabort = tx.onerror = () => reject(failure || tx.error || fail('Browser save failed. Download the draft as JSON.'));
      const abort = error => { failure = error; tx.abort(); };
      try { work(tx, value => { result = value; }, abort); } catch (error) { abort(error); }
    });
  }

  async function initialize() {
    const response = await fetch(new URL('samples.json', document.baseURI));
    if (!response.ok) throw fail('Cannot load the public sample catalog.');
    catalog = await response.json();
    if (!catalog.sample || catalog.schema_version !== 1) throw fail('Unsupported public sample.');
    if (!globalThis.indexedDB) throw fail('Storage is unavailable in this browser. Allow site storage and reopen the app.');
    connection = await new Promise((resolve, reject) => {
      const request = indexedDB.open(`voku-public-review:${scope}:${catalog.dataset_id}`, 1);
      request.onupgradeneeded = () => {
        const db = request.result;
        db.createObjectStore('reviews', {keyPath: 'page_id'});
        db.createObjectStore('history', {keyPath: 'id', autoIncrement: true}).createIndex('page_id', 'page_id');
        db.createObjectStore('settings', {keyPath: 'key'});
      };
      request.onerror = () => reject(fail('Cannot open browser storage. Allow site storage and reopen the app.'));
      request.onblocked = () => reject(fail('Close other tabs and reopen storage.'));
      request.onsuccess = () => resolve(request.result);
    });
    connection.onversionchange = () => connection.close();
    await transaction(['reviews', 'history'], 'readwrite', tx => {
      const reviews = tx.objectStore('reviews'), history = tx.objectStore('history');
      for (const page of catalog.pages) {
        const request = reviews.get(page.page_id);
        request.onsuccess = () => {
          const previous = request.result;
          if (!previous) {
            reviews.put({...page, status: 'unreviewed', issues: [], note: '', boxes: [], revision: 0,
              generation: 1, available: 1, source_condition: '', updated_at: null});
          } else if (previous.fingerprint !== page.fingerprint) {
            const now = new Date().toISOString();
            history.add({page_id: page.page_id, created_at: now, event: 'source_changed', snapshot: previous});
            reviews.put({...page, status: 'needs_review', issues: [], note: '', boxes: [],
              revision: previous.revision + 1, generation: previous.generation + 1, available: 1,
              source_condition: '', source_changed_at: now, updated_at: now});
          }
        };
      }
    });
  }
  // Initialize lazily, so startup failures are caught and displayed by the original UI.
  let ready;
  async function ensureReady() { await (ready ||= initialize()); }

  function read(store, key) {
    return transaction([store], 'readonly', (tx, done) => {
      const request = key === undefined ? tx.objectStore(store).getAll() : tx.objectStore(store).get(key);
      request.onsuccess = () => done(request.result);
    });
  }
  function validate(body, row) {
    if (!row) throw fail('Public sample page not found.', 404);
    if (body.fingerprint !== row.fingerprint || body.revision !== row.revision)
      throw fail('Another tab or sample version has changed. Keep your draft and check the latest records.', 409);
    if (!STATUSES.includes(body.status) || !Array.isArray(body.issues) || body.issues.some(x => !ISSUES.includes(x)))
      throw fail('Invalid status or issue type.');
    if (typeof body.note !== 'string' || body.note.length > 50000 || !Array.isArray(body.boxes) || body.boxes.length > 500)
      throw fail('Note or BBOX limit exceeded.');
    const ids = new Set();
    const boxes = body.boxes.map(box => {
      if (!box || typeof box.id !== 'string' || !box.id || box.id.length > 80 || ids.has(box.id)) throw fail('Invalid BBOX ID');
      ids.add(box.id);
      if (!['x','y','width','height'].every(key => Number.isInteger(box[key]))) throw fail('Invalid BBOX coordinates');
      const {x, y, width, height} = box;
      if (x < 0 || y < 0 || width < 1 || height < 1 || x + width > row.width || y + height > row.height)
        throw fail('BBOX extends outside the image.');
      if (!Number.isInteger(box.color) || box.color < 0 || box.color > 100000) throw fail('Invalid BBOX color');
      if (typeof box.name !== 'string' || box.name.length > 200) throw fail('BBOX names must be 200 characters or fewer.');
      return {id: box.id, x, y, width, height, color: box.color, name: box.name};
    });
    if (body.status === 'ok' && (body.issues.length || boxes.length)) throw fail('Clear issue types and BBOXes before saving as OK.');
    return {status: body.status, issues: [...new Set(body.issues)], note: body.note, boxes};
  }
  function save(body) {
    // A single IndexedDB transaction serializes writes from tabs, including revision checks.
    return transaction(['reviews', 'history'], 'readwrite', (tx, done, abort) => {
      const reviews = tx.objectStore('reviews'), history = tx.objectStore('history');
      const request = reviews.get(body.page_id);
      request.onsuccess = () => {
        try {
          const row = request.result, change = validate(body, row);
          if (Object.keys(change).every(key => JSON.stringify(change[key]) === JSON.stringify(row[key]))) { done(row); return; }
          const now = new Date().toISOString();
          history.add({page_id: row.page_id, created_at: now, event: 'before_edit', snapshot: copy(row)});
          const updated = {...row, ...change, revision: row.revision + 1, updated_at: now,
            reviewed_fingerprint: ['ok','issue'].includes(change.status) ? row.fingerprint : null};
          reviews.put(updated);
          history.add({page_id: row.page_id, created_at: now, event: 'saved', snapshot: copy(updated)});
          done(updated);
        } catch (error) { abort(error); }
      };
    });
  }
  const fileOrder = (a, b) => a.page_id.localeCompare(b.page_id);
  function filter(rows, query) {
    const status = query.get('status'), search = (query.get('q') || '').trim().normalize('NFC').toLocaleLowerCase();
    return rows.filter(row => (!STATUSES.includes(status) || row.status === status) &&
      `${row.page_id} ${row.filename} ${row.document}`.normalize('NFC').toLocaleLowerCase().includes(search));
  }
  function download(rows, history) {
    const content = rows.map(row => JSON.stringify({...row, schema_version: 1,
      source: {kind: 'public-sample', dataset_id: catalog.dataset_id}, annotation_target: 'final'})).join('\n') + (rows.length ? '\n' : '');
    const url = URL.createObjectURL(new Blob([content], {type: 'application/x-ndjson;charset=utf-8'}));
    const filename = `public-${history ? 'history' : 'reviews'}-${new Date().toISOString().replace(/[:.]/g, '-')}.jsonl`;
    const anchor = document.createElement('a');
    anchor.href = url; anchor.download = filename; anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    return {filename, path: filename, count: rows.length};
  }
  async function request(path, body) {
    await ensureReady();
    // These route names are the original UI's internal interface; they are never fetched.
    const route = new URL(path, location.href), q = route.searchParams;
    if (route.pathname === '/api/review') return save(body);
    if (route.pathname === '/api/session') return transaction(['settings'], 'readwrite', (tx, done) => {
      tx.objectStore('settings').put({key: 'session', value: copy(body)}); done({saved: true});
    });
    if (route.pathname === '/api/image') {
      const row = await read('reviews', q.get('page_id'));
      if (!row) throw fail('Public sample page not found.', 404);
      return row;
    }
    if (route.pathname === '/api/history') {
      const rows = (await read('history')).filter(row => row.page_id === q.get('page_id')).reverse();
      const offset = Math.max(0, Number(q.get('offset')) || 0);
      return {items: rows.slice(offset, offset + 30), total: rows.length, offset};
    }
    if (route.pathname === '/api/export') return download(await read(body.history ? 'history' : 'reviews'), body.history);
    if (route.pathname === '/api/sync') return {started: false};
    const rows = (await read('reviews')).sort(fileOrder);
    if (route.pathname === '/api/stats') {
      const counts = Object.fromEntries(STATUSES.map(status => [status, rows.filter(row => row.status === status).length]));
      return {counts: {...counts, total: rows.length, unavailable: 0}, sync: {},
        settings: {dataset_id: `${catalog.dataset_id}:${scope}`, session: (await read('settings', 'session'))?.value || {}}};
    }
    const matched = filter(rows, q);
    if (route.pathname === '/api/images') {
      const recent = ['ok', 'issue'].includes(q.get('status'));
      if (recent) matched.sort((a, b) => (b.updated_at || '').localeCompare(a.updated_at || '') || fileOrder(a, b));
      const limit = Math.min(100, Math.max(1, Number(q.get('limit')) || 60)), total = matched.length;
      const last = total ? Math.floor((total - 1) / limit) * limit : 0;
      let offset = Math.min(last, Math.max(0, Number(q.get('offset')) || 0));
      if (q.get('edge') === 'first') offset = 0;
      if (q.get('edge') === 'last') offset = last;
      return {items: matched.slice(offset, offset + limit), total, offset, limit, sort: recent ? 'recent_review' : 'filename'};
    }
    if (route.pathname === '/api/neighbor') {
      const direction = q.get('direction'), current = rows.find(row => row.page_id === q.get('page_id'));
      const candidates = direction === 'unreviewed' && !q.get('status') ? matched.filter(row => row.status === 'unreviewed') : matched;
      const eligible = current ? candidates.filter(row => direction === 'previous' ? fileOrder(row, current) < 0 : fileOrder(row, current) > 0) : candidates;
      let next = direction === 'previous' ? eligible.at(-1) : eligible[0];
      if (!next && direction === 'unreviewed') next = candidates[0];
      return {page_id: next?.page_id || null};
    }
    throw fail('Unsupported review action.');
  }
  return {request};
})();
