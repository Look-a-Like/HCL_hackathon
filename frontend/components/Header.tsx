"use client";

export default function Header() {
  return (
    <header className="sticky top-0 z-30 bg-white/80 backdrop-blur-md border-b border-[#E5E7EB] px-6 py-3 flex items-center gap-4">
      {/* Logo */}
      <div className="flex items-center gap-2.5 flex-shrink-0">
        <div className="w-8 h-8 rounded-xl flex items-center justify-center" style={{ background: "linear-gradient(135deg, #7C3AED 0%, #8B5CF6 100%)", boxShadow: "0 4px 12px rgba(124,58,237,0.3)" }}>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="12" r="10" />
            <line x1="2" y1="12" x2="22" y2="12" />
            <path d="M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20" />
          </svg>
        </div>
        <span className="font-bold text-[15px] text-[#1E1B4B]">Cartographer AI</span>
      </div>

      {/* Search */}
      <div className="flex-1 max-w-sm relative mx-4">
        <svg className="absolute left-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input type="text" placeholder="Query itinerary or ask agent..." className="nav-search" />
      </div>

      {/* Right icons */}
      <div className="ml-auto flex items-center gap-2">
        {[
          /* Bell */
          <path key="bell" d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" />,
          /* History */
          <>
            <polyline key="h1" points="1 4 1 10 7 10" />
            <path key="h2" d="M3.51 15a9 9 0 101.85-4.71L1 10" />
          </>,
          /* Settings */
          <>
            <circle key="s1" cx="12" cy="12" r="3" />
            <path key="s2" d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z" />,
          </>,
        ].map((paths, i) => (
          <button key={i} className="nav-icon-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              {paths}
            </svg>
          </button>
        ))}
        <div className="w-8 h-8 rounded-full flex items-center justify-center text-white text-[11px] font-bold ml-1" style={{ background: "linear-gradient(135deg, #7C3AED, #8B5CF6)" }}>
          CA
        </div>
      </div>
    </header>
  );
}
