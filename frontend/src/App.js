import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TempMail from "./TempMail";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TempMail />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
