import { Link, useLocation } from 'react-router-dom';
import { Button } from './ui/button';
import { Home, BarChart3, Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import logo from '../assets/logo.png';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();
  const { theme, setTheme } = useTheme();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-10 h-10 overflow-hidden ">
                <img src={logo} alt="WingstopFreeFries Logo" className="w-full h-full object-cover" />
              </div>
              <span className="text-xl font-bold text-gradient">WingstopFreeFries</span>
            </Link>

            <div className="flex items-center space-x-4">
              <Button
                variant={isActive('/') ? 'default' : 'ghost'}
                size="sm"
                asChild
              >
                <Link to="/" className="flex items-center space-x-2">
                  <Home className="w-4 h-4" />
                  <span className="hidden sm:inline">Home</span>
                </Link>
              </Button>

              <Button
                variant={isActive('/stats') ? 'default' : 'ghost'}
                size="sm"
                asChild
              >
                <Link to="/stats" className="flex items-center space-x-2">
                  <BarChart3 className="w-4 h-4" />
                  <span className="hidden sm:inline">Stats</span>
                </Link>
              </Button>
              
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
                className="flex items-center space-x-2"
              >
                {theme === 'dark' ? (
                  <Sun className="w-4 h-4" />
                ) : (
                  <Moon className="w-4 h-4" />
                )}
                <span className="hidden sm:inline">
                  {theme === 'dark' ? 'Light' : 'Dark'}
                </span>
              </Button>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="border-t border-border bg-background/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center text-sm text-muted-foreground">
            <p>WingstopFreeFries.xyz </p>
            <p className="mt-2">Contact <a href="mailto:foodsurveycodes@gmail.com">foodsurveycodes@gmail.com</a> if the site is broken</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;