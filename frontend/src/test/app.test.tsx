import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App } from "../app/App";

function renderApp() {
  const queryClient = new QueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );
}

describe("App", () => {
  it("renders the product shell", () => {
    renderApp();

    expect(screen.getByText("Research Copilot")).toBeInTheDocument();
    expect(screen.getByText(/Prepare sharper business meetings/)).toBeInTheDocument();
    expect(screen.getByText("Track workflow progress")).toBeInTheDocument();
  });
});

