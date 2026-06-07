import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000/api" });

export const getFlights = (scenario = "dense") =>
    API.get(`/flights?scenario=${scenario}`).then(r => r.data);

export const getSequence = (scenario = "dense", algorithm = "greedy") =>
    API.get(`/sequence?scenario=${scenario}&algorithm=${algorithm}`).then(r => r.data);

export const compareAlgorithms = (scenario = "dense") =>
    API.get(`/compare?scenario=${scenario}`).then(r => r.data);