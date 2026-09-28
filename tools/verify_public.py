"""Check public files, links, photo metadata and current demo/OCR hashes.

It reads files only and does not import historical production modules.
"""
from pathlib import Path
from html.parser import HTMLParser
import ast, hashlib, json, os, re, sys
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parents[1]

def nonpublic(path):
    parts={'.git','.DS_Store','__MACOSX','__pycache__','.venv','node_modules',
           'research','.history-edit','.review-check','.integration-check','.release-edit'}
    suffixes={'.pyc','.sqlite','.sqlite3','.db','.db-wal','.db-shm','.log','.tmp',
              '.swp','.swo','.zip','.ttf','.ttc','.otf','.woff','.woff2'}
    return (any(p in parts or (p.startswith('.') and p not in {'.gitignore','.nojekyll'}) for p in path.parts)
            or path.suffix.lower() in suffixes or path.name.endswith('~'))

def release_candidates():
    names=set()
    for directory,dirs,files in os.walk(ROOT):
        parent=Path(directory).relative_to(ROOT)
        dirs[:]=[d for d in dirs if not nonpublic(parent/d)]
        names.update((parent/f).as_posix() for f in files if not nonpublic(parent/f))
    return names

def markdown_anchors(text):
    anchors=set(re.findall(r'\bid=["\']([^"\']+)["\']',text));counts={}
    for heading in re.findall(r'^#{1,6}\s+(.+)',text,re.M):
        heading=re.sub(r'<[^>]+>','',heading).strip().rstrip('#').strip()
        slug=re.sub(r'[^\w\- ]','',heading.lower()).replace(' ','-')
        count=counts.get(slug,0);counts[slug]=count+1
        anchors.add(slug+(f'-{count}' if count else ''))
    return anchors

def metadata_free_webp_size(data):
    """Read the dimensions of a single image-only WebP, without a codec dependency.

    Publication photos have one VP8/VP8L chunk. Reject metadata, animation,
    unknown chunks and trailing bytes rather than silently skipping them.
    """
    if (len(data)<20 or data[:4]!=b'RIFF' or data[8:12]!=b'WEBP'
            or int.from_bytes(data[4:8],'little')+8!=len(data)):
        raise ValueError('Invalid WebP container length or signature')
    tag=data[12:16];size=int.from_bytes(data[16:20],'little')
    if 20+size+(size%2)!=len(data):
        raise ValueError('Photo contains extra chunks, metadata or invalid image length')
    frame=data[20:20+size]
    if tag==b'VP8 ' and len(frame)>=10 and frame[3:6]==b'\x9d\x01\x2a' and not frame[0]&1:
        dims=(int.from_bytes(frame[6:8],'little')&0x3fff,int.from_bytes(frame[8:10],'little')&0x3fff)
    elif tag==b'VP8L' and len(frame)>=5 and frame[0]==0x2f:
        bits=int.from_bytes(frame[1:5],'little');dims=((bits&0x3fff)+1,((bits>>14)&0x3fff)+1)
    else:
        raise ValueError('Photo is not a single VP8/VP8L image-only file')
    if min(dims)<=0:raise ValueError('Invalid photo dimensions')
    return dims

def main():
    names=(ROOT/'public-files.txt').read_text().splitlines()
    errors=[]
    if len(names)!=len(set(names)):errors.append('Duplicate allowlist entry')
    for name in names:
        path=Path(name)
        if not name or path.is_absolute() or '..' in path.parts or path.as_posix()!=name or nonpublic(path):
            errors.append('Private, temporary or invalid allowlist entry: '+name)
    for name in sorted(release_candidates()-set(names)):
        errors.append('File missing from public allowlist: '+name)
    patterns={
        'absolute_personal_path':re.compile('/'+'(?:Users|home)/[^\\s/]+'),
        'credential':re.compile(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)'),
        'email':re.compile(r'[A-Za-z0-9_.+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
        'operational_id':re.compile(r'\b(?:p|d|R|U)-[0-9a-f]{12,}\b'),
    }
    text_files=0; links=0;python_files=0;json_files=0
    def check_link(source,ref):
        nonlocal links
        parts=urlsplit(ref.strip('<>'))
        if parts.scheme or parts.netloc:return
        target=(source.parent/unquote(parts.path)).resolve() if parts.path else source
        links+=1
        if not target.is_relative_to(ROOT) or not target.exists():
            errors.append('Broken local link in '+source.relative_to(ROOT).as_posix()+': '+ref)
        elif target.is_file() and target.relative_to(ROOT).as_posix() not in names:
            errors.append('Link target missing from public allowlist: '+ref)
        elif parts.fragment and target.suffix=='.md' and unquote(parts.fragment) not in markdown_anchors(target.read_text()):
            errors.append('Missing Markdown anchor in '+source.relative_to(ROOT).as_posix()+': '+ref)
    class Links(HTMLParser):
        def handle_starttag(self,tag,attrs):
            for key,value in attrs:
                if key in {'href','src'} and value:
                    if value.startswith('/'):errors.append('HTML link loses project subpath: '+value)
                    check_link(self.source,value)
    for name in names:
        p=ROOT/name
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(ROOT):
            errors.append('Invalid release file: '+name);continue
        if p.suffix not in {'.md','.py','.json','.js','.cjs','.css','.html','.swift','.txt'} and p.name not in {'.gitignore','.nojekyll','SHA256SUMS'}:continue
        text=p.read_text();text_files+=1
        for kind,pattern in patterns.items():
            for match in pattern.finditer(text):
                if kind=='email' and match.group()=='contact@example.invalid':continue
                errors.append(kind+' in '+name+' line '+str(text[:match.start()].count('\n')+1))
        if p.suffix=='.py':
            ast.parse(text,filename=name);python_files+=1
        if p.suffix=='.json':
            json.loads(text);json_files+=1
        if p.suffix=='.md':
            for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)',text):
                check_link(p,match.group(1))
        if p.suffix=='.html':
            parser=Links();parser.source=p;parser.feed(text)
    photo_names=[name for name in names if name.startswith('history/assets/photos/')]
    if len(photo_names)!=19:errors.append('Expected 18 public photos and one representative strip')
    photo_files=0;strip_size=None
    for name in photo_names:
        p=ROOT/name
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*\.webp',p.name):
            errors.append('Photo filename must be a public WebP slug: '+name);continue
        if p.is_symlink() or not p.is_file() or not p.resolve().is_relative_to(ROOT):continue
        try:
            dims=metadata_free_webp_size(p.read_bytes());photo_files+=1
            if p.name=='archive-process-strip.webp':
                strip_size=list(dims)
                if dims!=(2520,1080):errors.append('Unexpected representative strip size')
            elif max(dims)>1600:errors.append('Public photo exceeds the 1600px viewing size: '+name)
        except ValueError as exc:errors.append('Photo validation failed: '+name+': '+str(exc))
    if strip_size is None:errors.append('Representative photo strip is missing or invalid')
    for item in json.loads((ROOT/'history/reference/code-provenance.json').read_text()):
        p=ROOT/'history/historical'/item['artifact']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['export_sha256']:
            errors.append('Historical export hash changed: '+item['artifact'])
    anchor_path='history/history-anchor.json'
    anchor=json.loads((ROOT/anchor_path).read_text())
    expected_history={name for name in names if name.startswith(('history/','korean/history/')) and name!=anchor_path}
    if set(anchor['files'])!=expected_history:
        errors.append('History anchor inventory differs from the allowlisted history files')
    for name,digest in anchor['files'].items():
        p=ROOT/name
        if name not in names or not p.is_file() or not p.resolve().is_relative_to(ROOT):
            errors.append('Invalid history anchor file: '+name)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
            errors.append('History anchor changed: '+name)
    digests={}
    def check_hash(path,expected):
        if (path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(ROOT)
                or path.resolve().relative_to(ROOT).as_posix() not in names):
            errors.append('Hash target outside public files: '+str(path.relative_to(ROOT)));return
        if path not in digests:digests[path]=hashlib.sha256(path.read_bytes()).hexdigest()
        if digests[path]!=expected:errors.append('Hash mismatch: '+path.relative_to(ROOT).as_posix())
    manifest_name='workflow/assets/demo/asset-manifest.json'
    manifest=json.loads((ROOT/manifest_name).read_text())
    if manifest['base']!='workflow':errors.append('Unexpected current asset manifest base')
    expected_assets={n.removeprefix('workflow/') for n in names if n.startswith('workflow/') and n!=manifest_name}
    if set(manifest['files'])!=expected_assets:errors.append('Current asset manifest differs from public workflow inventory')
    for name,item in manifest['files'].items():
        p=ROOT/'workflow'/name;check_hash(p,item['sha256'])
        if p.is_file() and p.stat().st_size!=item['bytes']:errors.append('Asset byte size mismatch: '+name)
    demo=ROOT/'workflow/assets/demo';episode_files=0;demo_pages=0;ocr_links=0;ocr_mirrors=0
    for year,physical,logical in [('1994',19,19),('2003',17,17),('2017',13,17)]:
        bundle=demo/year/'complete';prefix=bundle.relative_to(ROOT).as_posix()+'/'
        recorded=json.loads((bundle/'manifest.json').read_text())
        expected={n.removeprefix(prefix) for n in names if n.startswith(prefix) and n!=prefix+'manifest.json'}
        if set(recorded)!=expected:errors.append('Episode manifest inventory mismatch: '+year)
        for name,digest in recorded.items():check_hash(bundle/name,digest);episode_files+=1
        page_map=json.loads((bundle/'page-map.json').read_text());mapped={p['filename']:p for p in page_map}
        operations=json.loads((bundle/'operations.json').read_text())['pages']
        if (len(page_map)!=logical or len(mapped)!=logical or len(operations)!=logical or
                {p['physical_pdf_page'] for p in page_map}!=set(range(1,physical+1)) or
                {p['filename'] for p in operations}!=set(mapped)):
            errors.append('Demo page/operation inventory mismatch: '+year)
        for page in operations:
            for view,key,map_key in [('demo-source-safe','safe_input_sha256','safe_sha256'),('final','final_sha256','final_sha256')]:
                path=bundle/view/page['filename'];check_hash(path,page[key]);check_hash(path,mapped[page['filename']][map_key])
            demo_pages+=1
        for view,image_dir in [('safe','demo-source-safe'),('final','final')]:
            source=bundle/'ocr'/(view+'.json');ocr=json.loads(source.read_text());pages=ocr['pages']
            if ocr['pageCount']!=logical or len(pages)!=logical or {p['filename'] for p in pages}!=set(mapped):
                errors.append('OCR page inventory mismatch: '+year+'/'+view)
            for page in pages:
                path=bundle/image_dir/page['filename']
                if page['sourceRel']!=path.relative_to(demo).as_posix():errors.append('OCR source path mismatch: '+year+'/'+page['filename'])
                check_hash(path,page['sourceSHA256']);ocr_links+=1
            if (demo/year/(view+'-ocr.json')).read_bytes()!=source.read_bytes():errors.append('OCR public mirror differs: '+year+'/'+view)
            ocr_mirrors+=1
    release_hashes=0
    checksums={}
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        match=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
        if not match:
            errors.append('Invalid release checksum row');continue
        digest,name=match.groups()
        if name in checksums:errors.append('Duplicate release checksum: '+name)
        checksums[name]=digest
    if set(checksums)!=set(names)-{'SHA256SUMS'}:
        errors.append('Release checksum inventory differs from public allowlist')
    for name,digest in checksums.items():
        if name not in names:continue
        check_hash(ROOT/name,digest);release_hashes+=1
    result={'passed':not errors,'history_anchor':anchor['version'],'history_files_checked':len(anchor['files']),'allowlisted_files':len(names),'text_files_scanned':text_files,
        'local_links_checked':links,'python_files_parsed':python_files,'json_files_parsed':json_files,
        'asset_manifest_files_checked':len(manifest['files']),'episode_manifest_files_checked':episode_files,
        'metadata_free_photo_webps_checked':photo_files,'representative_strip_pixels':strip_size,
        'demo_pages_checked':demo_pages,'ocr_image_links_checked':ocr_links,'ocr_mirrors_checked':ocr_mirrors,'release_hashes_checked':release_hashes,'errors':errors,
        'scope':'Public inventory, text/privacy patterns, links, syntax, photo container metadata, current manifests and demo image/OCR bindings; no production execution or full privacy review.'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors:sys.exit(1)

if __name__=='__main__':main()
