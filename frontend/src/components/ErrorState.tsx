type ErrorStateProps = {
  title: string;
  body?: string;
};

export function ErrorState({ title, body = "Try again in a moment." }: ErrorStateProps) {
  return (
    <section className="state-message state-message--error" role="alert">
      <h2>{title}</h2>
      <p>{body}</p>
    </section>
  );
}

