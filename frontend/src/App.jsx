import { BrowserRouter, Routes, Route } from "react-router-dom";
import PlayerPage from "./pages/PlayerPage";
import ComparePage from "./pages/ComparePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/player/:id" element={<PlayerPage />} />
        <Route path="/compare" element={<ComparePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
