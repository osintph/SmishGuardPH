<template>
  <div class="grid md:grid-cols-5 gap-6">
    
    <div class="md:col-span-2 space-y-4">
      <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-md border-t-4 border-[#FCD116] dark:border-yellow-500">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">{{ $t('edu.what_title') }}</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed">{{ $t('edu.what_desc') }}</p>
      </div>
      
      <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-md border-t-4 border-[#0038A8] dark:border-blue-500">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-2">{{ $t('edu.how_title') }}</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 leading-relaxed whitespace-pre-line">{{ $t('edu.how_desc') }}</p>
      </div>
    </div>

    <div class="md:col-span-3 bg-white dark:bg-slate-800 p-6 sm:p-8 rounded-2xl shadow-xl border border-gray-100 dark:border-slate-700 relative overflow-hidden">
      <div class="absolute top-0 right-0 w-32 h-32 bg-[#CE1126] opacity-5 rounded-bl-full pointer-events-none"></div>

      <h2 class="text-2xl font-extrabold mb-2 text-[#0038A8] dark:text-blue-400">{{ $t('form.heading') }}</h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6 text-sm">{{ $t('form.subheading') }}</p>

      <div v-if="showSuccess" class="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg flex items-start gap-3 animate-fade-in">
        <span class="text-xl">✅</span>
        <p class="font-medium text-sm">{{ $t('form.success') }}</p>
      </div>

      <form @submit.prevent="submitForm" class="space-y-4">
        <div>
          <label class="block mb-1 text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('form.sender_label') }}</label>
          <input v-model="form.sender" type="text" placeholder="e.g. 0917... or Maya" required class="w-full p-3 border border-gray-300 rounded-lg dark:bg-slate-900 dark:border-slate-600 focus:ring-2 focus:ring-[#0038A8] outline-none transition-all">
        </div>
        <div>
          <label class="block mb-1 text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('form.message_label') }}</label>
          <textarea v-model="form.message" rows="4" placeholder="Paste the exact scam text message here..." required class="w-full p-3 border border-gray-300 rounded-lg dark:bg-slate-900 dark:border-slate-600 resize-none focus:ring-2 focus:ring-[#0038A8] outline-none transition-all"></textarea>
        </div>
        <button type="submit" :disabled="loading" class="w-full bg-[#0038A8] hover:bg-blue-800 text-white py-3 rounded-lg font-bold shadow-md transition-all flex justify-center items-center gap-2 disabled:opacity-70">
          <span>{{ loading ? $t('form.processing') : $t('form.submit_btn') }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const form = ref({ sender: '', message: '' });
const loading = ref(false);
const showSuccess = ref(false);

const submitForm = async () => {
  loading.value = true;
  showSuccess.value = false;
  
  try {
    const res = await fetch('/api/report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    });
    
    if (res.ok) {
      showSuccess.value = true;
      form.value = { sender: '', message: '' };
      setTimeout(() => { showSuccess.value = false; }, 5000);
    }
  } catch (err) { console.error(err); } 
  finally { loading.value = false; }
};
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-in-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>