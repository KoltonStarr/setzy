import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import "./app.css";

export default function App() {
  return (
    <Router
      root={props => (
        <>
          <h1>hello</h1>
        </>
      )}
    >
      <FileRoutes />
    </Router>
  );
}
