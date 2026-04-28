import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  "https://thgfzwqvwiddnoduyote.supabase.co",
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRoZ2Z6d3F2d2lkZG5vZHV5b3RlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczNDQ4NDYsImV4cCI6MjA5MjkyMDg0Nn0.3mXg0v09kLsWBzGXjj0RbQL2Le-_uFxHYE_BBFyYJ4c"
);