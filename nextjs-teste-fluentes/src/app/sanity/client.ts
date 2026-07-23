import { createClient } from "next-sanity";

export const client = createClient({
  projectId: "vo3zcq0s",
  dataset: "production",
  apiVersion: "2026-05-15",
  useCdn: false,
});