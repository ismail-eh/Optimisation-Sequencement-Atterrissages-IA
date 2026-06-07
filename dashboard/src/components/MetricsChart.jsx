import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid,
    Tooltip, Legend, ResponsiveContainer
} from "recharts";

export default function MetricsChart({ comparison }) {
    if (!comparison) return null;

    const data = [
        {
            name: "Total attente",
            FCFS: comparison.results.fcfs.metrics.total_wait_min,
            GREEDY: comparison.results.greedy.metrics.total_wait_min,
            GENETIC: comparison.results.genetic.metrics.total_wait_min,
        },
        {
            name: "Moy attente",
            FCFS: comparison.results.fcfs.metrics.avg_wait_min,
            GREEDY: comparison.results.greedy.metrics.avg_wait_min,
            GENETIC: comparison.results.genetic.metrics.avg_wait_min,
        },
        {
            name: "Séparation min",
            FCFS: comparison.results.fcfs.metrics.min_separation,
            GREEDY: comparison.results.greedy.metrics.min_separation,
            GENETIC: comparison.results.genetic.metrics.min_separation,
        },
    ];

    return (
        <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis dataKey="name" tick={{ fill: "#9ca3af", fontSize: 11 }} />
                <YAxis tick={{ fill: "#9ca3af" }} />
                <Tooltip
                    contentStyle={{ background: "#1f2937", border: "none", borderRadius: 8 }}
                    labelStyle={{ color: "#f3f4f6" }}
                />
                <Legend wrapperStyle={{ color: "#9ca3af" }} />
                <Bar dataKey="FCFS" fill="#ef4444" radius={[4, 4, 0, 0]} />
                <Bar dataKey="GREEDY" fill="#22c55e" radius={[4, 4, 0, 0]} />
                <Bar dataKey="GENETIC" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
        </ResponsiveContainer>
    );
}