import { FormEvent, useState } from "react";
import { Plus } from "lucide-react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createSession } from "../../lib/api";

type SessionCreateFormProps = {
  onCreated: (sessionId: string) => void;
};

export function SessionCreateForm({ onCreated }: SessionCreateFormProps) {
  const queryClient = useQueryClient();
  const [companyName, setCompanyName] = useState("");
  const [website, setWebsite] = useState("");
  const [objective, setObjective] = useState("");
  const mutation = useMutation({
    mutationFn: createSession,
    onSuccess: async (session) => {
      await queryClient.invalidateQueries({ queryKey: ["sessions"] });
      onCreated(session.id);
      setCompanyName("");
      setWebsite("");
      setObjective("");
    }
  });

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    mutation.mutate({
      company_name: companyName,
      website,
      objective
    });
  }

  return (
    <form className="session-form" onSubmit={onSubmit}>
      <div className="form-row">
        <label htmlFor="company-name">Company</label>
        <input
          id="company-name"
          value={companyName}
          onChange={(event) => setCompanyName(event.target.value)}
          placeholder="Acme Corp"
          required
        />
      </div>
      <div className="form-row">
        <label htmlFor="website">Website</label>
        <input
          id="website"
          value={website}
          onChange={(event) => setWebsite(event.target.value)}
          placeholder="https://acme.example"
          required
          type="url"
        />
      </div>
      <div className="form-row">
        <label htmlFor="objective">Objective</label>
        <textarea
          id="objective"
          value={objective}
          onChange={(event) => setObjective(event.target.value)}
          placeholder="Prepare for a first discovery call"
          required
          rows={3}
        />
      </div>
      {mutation.isError ? (
        <p className="inline-error" role="alert">
          {mutation.error.message}
        </p>
      ) : null}
      <button className="primary-button" disabled={mutation.isPending} type="submit">
        <Plus aria-hidden="true" size={18} />
        {mutation.isPending ? "Creating" : "Create session"}
      </button>
    </form>
  );
}

