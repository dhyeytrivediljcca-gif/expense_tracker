import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function ExpenseHistory() {
  const navigate = useNavigate();
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadExpenses = async () => {
    try {
      const { data } = await api.get('/expenses');
      setExpenses(data);
    } catch (error) {
      if (error.response?.status === 401) {
        localStorage.removeItem('token');
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExpenses();
  }, [navigate]);

  if (loading) {
    return <div className="text-gray-600">Loading expenses...</div>;
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-semibold text-gray-900">Expense History</h1>
        <p className="mt-1 text-sm text-gray-500">Your latest expenses appear first.</p>
      </div>

      <div className="space-y-4">
        {expenses.length === 0 ? (
          <div className="rounded-2xl bg-white p-6 text-gray-500 shadow-sm">No expenses yet.</div>
        ) : (
          expenses.map((expense) => (
            <div key={expense.id} className="rounded-2xl bg-white p-5 shadow-sm">
              <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{expense.title}</h3>
                  <p className="text-sm text-gray-500">{expense.note || 'No note provided.'}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-semibold text-blue-600">₹{expense.amount.toFixed(2)}</p>
                  <p className="text-sm text-gray-500">{expense.date}</p>
                </div>
              </div>
              <div className="mt-4 flex flex-wrap gap-2 text-sm">
                <span className="rounded-full bg-blue-50 px-3 py-1 text-blue-700">Category: {expense.category}</span>
                <span className="rounded-full bg-gray-100 px-3 py-1 text-gray-600">Created: {new Date(expense.created_at).toLocaleDateString()}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
