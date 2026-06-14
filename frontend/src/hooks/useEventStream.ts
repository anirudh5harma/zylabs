import { useEffect } from "react";

type UseEventStreamOptions = {
  enabled: boolean;
  url: string;
  onMessage: () => void;
};

export function useEventStream({ enabled, url, onMessage }: UseEventStreamOptions) {
  useEffect(() => {
    if (!enabled || typeof EventSource === "undefined") return;

    const source = new EventSource(url);
    source.addEventListener("workflow", onMessage);
    source.addEventListener("done", () => source.close());
    source.onerror = () => source.close();

    return () => source.close();
  }, [enabled, onMessage, url]);
}

