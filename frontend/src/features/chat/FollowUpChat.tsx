import { FormEvent, useState } from "react";
import { Send } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { askFollowUp } from "../../lib/api";
import type { SessionDetail } from "../../lib/types";

type FollowUpChatProps = {
  session: SessionDetail;
  onMessageSent: () => void;
};

export function FollowUpChat({ session, onMessageSent }: FollowUpChatProps) {
  const [message, setMessage] = useState("");
  const mutation = useMutation({
    mutationFn: () => askFollowUp(session.id, message),
    onSuccess: () => {
      setMessage("");
      onMessageSent();
    }
  });

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!message.trim()) return;
    mutation.mutate();
  }

  const disabled = !session.report || mutation.isPending;

  return (
    <section className="workspace-section">
      <div className="section-heading">
        <h3>Follow-up chat</h3>
        <span>{session.chat_messages.length} messages</span>
      </div>
      <div className="chat-thread">
        {session.chat_messages.length === 0 ? (
          <p className="muted">
            {session.report ? "Ask a question about this report." : "Chat unlocks after the report is ready."}
          </p>
        ) : (
          session.chat_messages.map((item) => (
            <article className={`chat-message chat-message--${item.role}`} key={item.id}>
              <strong>{item.role === "user" ? "You" : "Response"}</strong>
              <p>{item.content}</p>
            </article>
          ))
        )}
      </div>
      <form className="chat-form" onSubmit={onSubmit}>
        <input
          aria-label="Follow-up question"
          disabled={disabled}
          onChange={(event) => setMessage(event.target.value)}
          placeholder={session.report ? "Ask about discovery, risks, or outreach" : "Run the workflow first"}
          value={message}
        />
        <button className="icon-button" disabled={disabled} type="submit">
          <Send aria-hidden="true" size={18} />
          <span className="sr-only">Send</span>
        </button>
      </form>
      {mutation.isError ? (
        <p className="inline-error" role="alert">
          {mutation.error.message}
        </p>
      ) : null}
    </section>
  );
}

