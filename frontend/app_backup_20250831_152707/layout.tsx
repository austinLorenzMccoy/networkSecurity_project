export const metadata = {
  title: 'Network Security Dashboard',
  description: 'Threat classification and monitoring UI',
};

import '../styles/globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
