import { useEffect, useState } from 'react';
import { getContainers, startContainer, stopContainer, getLogs } from './api';

interface Container {
  id: string;
  name: string;
  status: string;
  image: string[];
}

function App() {
  const [containers, setContainers] = useState<Container[]>([]);
  const [logs, setLogs] = useState<string>('');

  const fetchContainers = async () => {
    const data = await getContainers();
    setContainers(data);
  };

  const fetchLogs = async (id: string) => {
    const logData = await getLogs(id);
    setLogs(logData);
  };

  useEffect(() => {
    fetchContainers();
  }, []);

  return (
    <div className="flex flex-col w-full min-h-screen bg-gray-900 text-white p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">Bot Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full">
        {containers.map(container => (
          <div key={container.id} className="bg-gray-800 p-4 rounded shadow">
            <h2 className="text-xl font-semibold">{container.name}</h2>
            <p className="mt-1">
              Status:{' '}
              <span
                className={`font-bold ${
                  container.status === 'running' ? 'text-green-400' : 'text-red-400'
                }`}
              >
                {container.status}
              </span>
            </p>
            <p className="mt-1">Image: {container.image?.join(', ') || 'N/A'}</p>

            <div className="mt-4 space-x-2">
              <button
                className="bg-green-500 hover:bg-green-600 px-3 py-1 rounded"
                onClick={() => startContainer(container.id).then(fetchContainers)}
              >
                Start
              </button>
              <button
                className="bg-red-500 hover:bg-red-600 px-3 py-1 rounded"
                onClick={() => stopContainer(container.id).then(fetchContainers)}
              >
                Stop
              </button>
              <button
                className="bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded"
                onClick={() => fetchLogs(container.id)}
              >
                Logs
              </button>
            </div>
          </div>
        ))}
      </div>

      {logs && (
        <div className="mt-8 bg-gray-700 p-4 rounded shadow w-full">
          <h2 className="text-xl font-semibold mb-2">Container Logs</h2>
          <pre className="overflow-x-auto whitespace-pre-wrap">{logs}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
