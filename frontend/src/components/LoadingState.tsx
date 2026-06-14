type LoadingStateProps = {
  label: string;
};

export function LoadingState({ label }: LoadingStateProps) {
  return (
    <section className="state-message" aria-live="polite">
      <span className="loader" aria-hidden="true" />
      <p>{label}</p>
    </section>
  );
}

