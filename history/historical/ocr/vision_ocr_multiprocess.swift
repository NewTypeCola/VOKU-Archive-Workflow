import Foundation
import Vision
import ImageIO
import CryptoKit
import AppKit

struct SourcePage: Codable {
    let page: Int
    let filename: String
    let sourceRel: String
    let sha256: String
    let size: Int
    let mtimeNs: Int64
}
struct Group: Codable {
    let groupKey: String
    let year: String
    let semester: String
    let pages: [SourcePage]
}
struct Plan: Codable {
    let runID: String
    let createdAt: String
    let sourceRoot: String
    let outputRoot: String
    let totalPages: Int
    let groups: [Group]
}
struct Box: Codable { let x: Double; let y: Double; let width: Double; let height: Double }
struct Line: Codable { let text: String; let confidence: Float; let boundingBox: Box }
struct Page: Codable {
    let page: Int
    let filename: String
    let sourceRel: String
    let sourceSHA256: String
    let width: Int
    let height: Int
    let status: String
    let generatedAt: String
    let text: String
    let lines: [Line]
    let error: String?
}
struct Engine: Codable, Equatable {
    let name: String
    let revision: Int
    let recognitionLevel: String
    let recognitionLanguages: [String]
    let usesLanguageCorrection: Bool
    let boundingBoxCoordinateSystem: String
    let macOS: String
}
struct Document: Codable {
    let schemaVersion: String
    let runID: String
    let groupKey: String
    let year: String
    let semester: String
    let pageCount: Int
    let generatedAt: String
    let engine: Engine
    let status: String
    let pages: [Page]
}
let engine = Engine(name: "Apple Vision VNRecognizeTextRequest", revision: 3,
    recognitionLevel: "accurate", recognitionLanguages: ["ko-KR", "en-US"],
    usesLanguageCorrection: true, boundingBoxCoordinateSystem: "normalized_top_left_xywh",
    macOS: ProcessInfo.processInfo.operatingSystemVersionString)
func now() -> String { ISO8601DateFormatter().string(from: Date()) }
func sha(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }
func jsonWrite<T: Encodable>(_ item: T, _ url: URL) throws {
    let encoder = JSONEncoder(); encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]
    var data = try encoder.encode(item); data.append(10)
    try data.write(to: url, options: .atomic)
}
func linesFor(_ data: Data) throws -> (Int, Int, [Line]) {
    guard let source = CGImageSourceCreateWithData(data as CFData, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        throw NSError(domain: "FreshOCR", code: 1, userInfo: [NSLocalizedDescriptionKey: "image_decode_failed"])
    }
    let request = VNRecognizeTextRequest()
    request.revision = VNRecognizeTextRequestRevision3
    request.recognitionLevel = .accurate
    request.recognitionLanguages = engine.recognitionLanguages
    request.usesLanguageCorrection = engine.usesLanguageCorrection
    try VNImageRequestHandler(cgImage: image, options: [:]).perform([request])
    let lines = (request.results ?? []).compactMap { observation -> Line? in
        guard let top = observation.topCandidates(1).first else { return nil }
        let text = top.string.trimmingCharacters(in: .whitespacesAndNewlines)
        if text.isEmpty { return nil }
        let box = observation.boundingBox
        return Line(text: text, confidence: top.confidence, boundingBox: Box(
            x: Double(box.minX), y: Double(1 - box.maxY), width: Double(box.width), height: Double(box.height)))
    }
    return (image.width, image.height, lines)
}
func processPage(_ input: SourcePage, root: URL) -> Page {
    do {
        let data = try Data(contentsOf: root.appendingPathComponent(input.sourceRel))
        let digest = sha(data)
        guard data.count == input.size && digest == input.sha256 else {
            throw NSError(domain: "FreshOCR", code: 2, userInfo: [NSLocalizedDescriptionKey: "source_changed_since_inventory"])
        }
        let (width, height, lines) = try linesFor(data)
        return Page(page: input.page, filename: input.filename, sourceRel: input.sourceRel,
            sourceSHA256: digest, width: width, height: height, status: "success", generatedAt: now(),
            text: lines.map(\.text).joined(separator: "\n"), lines: lines, error: nil)
    } catch {
        return Page(page: input.page, filename: input.filename, sourceRel: input.sourceRel,
            sourceSHA256: input.sha256, width: 0, height: 0, status: "error", generatedAt: now(),
            text: "", lines: [], error: String(describing: error))
    }
}
final class State: @unchecked Sendable {
    let lock = NSLock()
    var pages = 0; var groups = 0; var errors = 0; var empty = 0; var lines = 0; var skipped = 0
    var stop = false; var lastLog = Date.distantPast
    let start = Date(); let plan: Plan; let workers: Int; let progress: URL
    init(_ plan: Plan, _ workers: Int) {
        self.plan = plan; self.workers = workers
        self.progress = CommandLine.arguments.count > 4 ? URL(fileURLWithPath: CommandLine.arguments[4]) : URL(fileURLWithPath: plan.outputRoot).appendingPathComponent("_work/progress.json")
    }
    func wantsStop() -> Bool { lock.lock(); defer {lock.unlock()}; return stop }
    func requestStop(_ reason: String) {
        lock.lock(); stop = true; log("stopping: \(reason)", force: true); lock.unlock()
    }
    func recordPage(_ page: Page) {
        lock.lock(); defer {lock.unlock()}
        pages += 1; lines += page.lines.count
        if page.status != "success" { errors += 1; stop = true }
        else if page.lines.isEmpty { empty += 1 }
        log(nil, force: false)
    }
    func recordGroup(_ document: Document, skipped isSkipped: Bool) {
        lock.lock(); defer {lock.unlock()}
        groups += 1
        if isSkipped {
            skipped += 1; pages += document.pages.count
            lines += document.pages.reduce(0) {$0 + $1.lines.count}
            empty += document.pages.filter {$0.lines.isEmpty}.count
        }
        log(nil, force: false)
    }
    func log(_ message: String?, force: Bool) {
        if !force && Date().timeIntervalSince(lastLog) < 5 { return }
        lastLog = Date()
        let progress: [String: Any] = ["runID": plan.runID, "updatedAt": now(),
            "status": stop ? "stopping" : (pages == plan.totalPages && groups == plan.groups.count ? "ocr_complete_pending_verification" : "running"),
            "pages": pages, "totalPages": plan.totalPages, "groups": groups, "totalGroups": plan.groups.count,
            "errors": errors, "emptyPages": empty, "lines": lines, "resumedGroups": skipped,
            "workers": workers, "elapsedSeconds": Date().timeIntervalSince(start)]
        if let data = try? JSONSerialization.data(withJSONObject: progress, options: [.sortedKeys]) {
            try? data.write(to: self.progress, options: .atomic)
            FileHandle.standardOutput.write(data); FileHandle.standardOutput.write(Data("\n".utf8))
        }
        if let message { FileHandle.standardError.write(Data((message + "\n").utf8)) }
    }
    func finish() {lock.lock(); log(nil, force: true); lock.unlock()}
}
func resumable(_ url: URL, _ group: Group, _ plan: Plan) -> Document? {
    guard let data = try? Data(contentsOf: url), let doc = try? JSONDecoder().decode(Document.self, from: data),
          doc.schemaVersion == "final-tri-force-fresh-ocr-v1", doc.runID == plan.runID,
          doc.groupKey == group.groupKey, doc.year == group.year, doc.semester == group.semester,
          doc.status == "complete", doc.engine == engine, doc.pageCount == group.pages.count,
          doc.pages.count == group.pages.count else { return nil }
    for (page, input) in zip(doc.pages, group.pages) {
        guard page.status == "success", page.error == nil, page.page == input.page,
              page.filename == input.filename, page.sourceRel == input.sourceRel,
              page.sourceSHA256 == input.sha256, page.width > 0, page.height > 0,
              page.text == page.lines.map(\.text).joined(separator: "\n") else { return nil }
    }
    return doc
}
let args = CommandLine.arguments
if args.count == 3 && args[1] == "--smoke" {
    let folder = URL(fileURLWithPath: args[2], isDirectory: true)
    let image = NSImage(size: NSSize(width: 1600, height: 400))
    image.lockFocus()
    NSColor.white.setFill(); NSRect(x: 0, y: 0, width: 1600, height: 400).fill()
    ("VISION OCR CHECK 24680" as NSString).draw(at: NSPoint(x: 70, y: 250),
        withAttributes: [.font: NSFont.systemFont(ofSize: 70), .foregroundColor: NSColor.black])
    ("한국어 방송 원고 확인" as NSString).draw(at: NSPoint(x: 70, y: 100),
        withAttributes: [.font: NSFont.systemFont(ofSize: 70), .foregroundColor: NSColor.black])
    image.unlockFocus()
    let rep = NSBitmapImageRep(data: image.tiffRepresentation!)!
    let data = rep.representation(using: .png, properties: [:])!
    try data.write(to: folder.appendingPathComponent("smoke.png"), options: .atomic)
    let (_, _, lines) = try linesFor(data)
    let recognized = lines.map(\.text).joined(separator: "\n")
    let passed = recognized.contains("24680") && recognized.contains("한국어")
    struct Smoke: Encodable { let passed: Bool; let engine: Engine; let generatedAt: String; let text: String; let lines: [Line] }
    try jsonWrite(Smoke(passed: passed, engine: engine, generatedAt: now(), text: recognized, lines: lines), folder.appendingPathComponent("smoke.json"))
    print("Vision synthetic smoke passed=\(passed), lines=\(lines.count)")
    exit(passed ? 0 : 1)
}
guard args.count >= 3 else { fatalError("usage: vision_ocr PLAN WORKERS [LIMIT_GROUPS]") }
let plan = try JSONDecoder().decode(Plan.self, from: Data(contentsOf: URL(fileURLWithPath: args[1])))
let workers = Int(args[2])!
guard workers > 0 && workers <= 16 else {fatalError("workers must be 1...16")}
let selected = args.count > 3 ? Array(plan.groups.prefix(Int(args[3])!)) : plan.groups
let state = State(plan, workers)
signal(SIGINT, SIG_IGN); signal(SIGTERM, SIG_IGN)
let interrupts = [SIGINT, SIGTERM].map { sig -> DispatchSourceSignal in
    let source = DispatchSource.makeSignalSource(signal: sig, queue: .global())
    source.setEventHandler {state.requestStop("signal \(sig), finishing active groups")}; source.resume(); return source
}
let queue = DispatchQueue(label: "fresh.ocr", attributes: .concurrent)
let semaphore = DispatchSemaphore(value: workers)
let jobs = DispatchGroup()
let outputRoot = URL(fileURLWithPath: plan.outputRoot, isDirectory: true)
let sourceRoot = URL(fileURLWithPath: plan.sourceRoot, isDirectory: true)
for group in selected {
    if state.wantsStop() {break}
    let output = outputRoot.appendingPathComponent(group.year).appendingPathComponent(group.groupKey + ".json")
    if let doc = resumable(output, group, plan) {state.recordGroup(doc, skipped: true); continue}
    if FileManager.default.fileExists(atPath: output.path) {
        state.requestStop("existing output did not pass resume validation: \(output.path)"); break
    }
    semaphore.wait()
    if state.wantsStop() {semaphore.signal(); break}
    jobs.enter()
    queue.async {
        defer {jobs.leave(); semaphore.signal()}
        var pages: [Page] = []
        for input in group.pages {
            let page = autoreleasepool {processPage(input, root: sourceRoot)}
            pages.append(page); state.recordPage(page)
            if page.status != "success" {break}
        }
        let doc = Document(schemaVersion: "final-tri-force-fresh-ocr-v1", runID: plan.runID,
            groupKey: group.groupKey, year: group.year, semester: group.semester,
            pageCount: pages.count, generatedAt: now(), engine: engine,
            status: pages.count == group.pages.count && pages.allSatisfy {$0.status == "success"} ? "complete" : "partial_error", pages: pages)
        do {
            try jsonWrite(doc, output)
            state.recordGroup(doc, skipped: false)
        } catch { state.requestStop("write failed: \(error)") }
    }
}
jobs.wait(); state.finish()
withExtendedLifetime(interrupts) {}
exit(state.wantsStop() ? 1 : 0)
