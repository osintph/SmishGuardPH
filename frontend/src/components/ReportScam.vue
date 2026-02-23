<template>
  <div class="min-h-screen text-gray-900 dark:text-gray-100 transition-colors">
    <nav class="bg-blue-700 dark:bg-slate-800 text-white p-4 flex justify-between items-center shadow-md">
      <div class="flex items-center gap-2"><div class="w-3 h-3 bg-yellow-400 rounded-full"></div><h1 class="font-bold">{{ $t('title') }}</h1></div>
      <div class="flex items-center gap-4">
        <select v-model="$i18n.locale" class="bg-blue-600 dark:bg-slate-700 rounded px-2 py-1 outline-none text-sm">
          <option value="en">EN</option><option value="fil">FIL</option>
        </select>
        <button @click="toggleDark" class="p-2 bg-blue-600 dark:bg-slate-700 rounded-full text-sm">🌙/☀️</button>
      </div>
    </nav>
    <main class="max-w-xl mx-auto mt-8 p-4">
      <div class="bg-white dark:bg-slate-800 p-6 rounded-xl shadow-lg border dark:border-slate-700">
        <h2 class="text-2xl font-bold mb-2">{{ $t('heading') }}</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">{{ $t('subheading') }}</p>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block mb-1 text-sm">{{ $t('sender_lbl') }}</label>
            <input v-model="form.sender" type="text" required class="w-full p-2 border rounded dark:bg-slate-900 dark:border-slate-600">
          </div>
          <div>
            <label class="block mb-1 text-sm">{{ $t('msg_lbl') }}</label>
            <textarea v-model="form.message" rows="4" required class="w-full p-2 border rounded dark:bg-slate-900 dark:border-slate-600 resize-none"></textarea>
          </div>
          <button type="submit" :disabled="loading" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded font-bold">
            {{ loading ? $t('processing') : $t('btn') }}
          </button>
        </form>
      </div>
    </main>
  </div>
</template>
<script setup>
import { ref } from 'vue';
const form = ref({ sender: '', message: '' });
const loading = ref(false);
const toggleDark = () => document.documentElement.classList.toggle('dark');
const submitForm = async () => {
  loading.value = true;
  try {
    const res = await fetch('/api/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    });
    if (res.ok) {
      alert('Report submitted to threat feed!');
      form.value = { sender: '', message: '' };
    }
  } catch (err) { console.error(err); } 
  finally { loading.value = false; }
};
</script>
