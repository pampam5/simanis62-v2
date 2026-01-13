import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { MacOSDashboardPage } from './pages/MacOSDashboardPage';
import { AssetsPage } from './pages/AssetsPage';
import { KIBPage } from './pages/KIBPage';
import { MutationPage } from './pages/MutationPage';
import { RoomsPage } from './pages/RoomsPage';
import { SettingsPage } from './pages/SettingsPage';
import { MacOSDesktopShell } from './components/layout/macos-desktop-shell';
import './styles/glass.css';

function App() {
  return (
    <BrowserRouter>
      <MacOSDesktopShell>
        <Routes>
          <Route path="/" element={<MacOSDashboardPage />} />
          <Route path="/aset" element={<AssetsPage />} />
          <Route path="/kib" element={<KIBPage />} />
          <Route path="/mutasi" element={<MutationPage />} />
          <Route path="/ruangan" element={<RoomsPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </MacOSDesktopShell>
    </BrowserRouter>
  );
}

export default App;
