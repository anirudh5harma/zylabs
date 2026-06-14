import type { ReactNode } from "react";

type AppShellProps = {
  sidebar: ReactNode;
  children: ReactNode;
};

export function AppShell({ sidebar, children }: AppShellProps) {
  return (
    <div className="app-frame">
      <aside className="sidebar" aria-label="Research sessions">
        <div className="brand-block">
          <p className="eyebrow">Research Copilot</p>
          <h1>Meeting briefings that keep their receipts.</h1>
        </div>
        {sidebar}
      </aside>
      <main className="workspace">{children}</main>
    </div>
  );
}

