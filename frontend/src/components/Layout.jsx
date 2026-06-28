import { NavLink, Outlet, useNavigate } from 'react-router-dom';

const links = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/expenses/add', label: 'Add Expense' },
  { to: '/expenses/history', label: 'Expense History' },
];

export default function Layout() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="mx-auto flex max-w-7xl flex-col lg:flex-row">
        <aside className="w-full border-b border-gray-200 bg-white p-4 sm:p-6 lg:min-h-screen lg:w-72 lg:border-b-0 lg:border-r">
          <div className="mb-4 flex flex-col gap-1 sm:mb-6">
            <h2 className="text-xl font-semibold text-blue-600">Student Expense Tracker</h2>
            <p className="text-sm text-gray-500">Simple budget tracking</p>
          </div>
          <nav className="flex flex-wrap gap-2 lg:flex-col lg:gap-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `block rounded-lg px-4 py-3 text-sm font-medium ${
                    isActive ? 'bg-blue-600 text-white' : 'text-gray-700 hover:bg-gray-100'
                  } lg:min-w-[0]`
                }
              >
                {link.label}
              </NavLink>
            ))}
            <button
              onClick={handleLogout}
              className="mt-2 block w-full rounded-lg bg-gray-800 px-4 py-3 text-left text-sm font-medium text-white lg:mt-4"
            >
              Logout
            </button>
          </nav>
        </aside>
        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
