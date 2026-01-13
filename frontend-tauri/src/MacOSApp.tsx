/**
 * SIMANIS62 - macOS Liquid Glass Style Demo App
 * 
 * This demonstrates the full macOS Liquid Glass design system
 * for the SIMANIS62 asset management application.
 */

import { MacOSMainLayout } from './components/layout';
import { MacOSDashboardPage } from './pages/MacOSDashboardPage';
import './styles/glass.css';

function MacOSApp() {
    return (
        <MacOSMainLayout>
            <MacOSDashboardPage />
        </MacOSMainLayout>
    );
}

export default MacOSApp;
