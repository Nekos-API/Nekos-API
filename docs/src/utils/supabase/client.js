import { createClient } from '@supabase/supabase-js';

var supabase = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL, process.env.NEXT_ANON_SUPABASE_KEY);

export default supabase;