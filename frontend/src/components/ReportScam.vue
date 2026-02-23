<template>
  <div class="grid md:grid-cols-5 gap-6 sm:gap-8">
    
    <div class="md:col-span-2 space-y-6">
      
      <div class="bg-[#0038A8] p-6 rounded-2xl shadow-lg border-b-4 border-[#CE1126] text-white relative overflow-hidden">
        <svg class="absolute -right-6 -top-6 w-32 h-32 text-[#FCD116] opacity-20 animate-pulse-slow" viewBox="0 0 100 100" fill="currentColor">
          <path d="M50 15L53 35L70 20L60 38L80 35L65 47L85 55L65 57L75 75L58 65L60 85L48 68L35 85L38 65L20 75L30 57L10 55L30 47L15 35L35 38L25 20L42 35Z"/>
          <circle cx="50" cy="50" r="15" />
        </svg>
        
        <h3 class="text-2xl font-black mb-1 tracking-wide text-[#FCD116]">Mabuhay! 🇵🇭</h3>
        <p class="text-sm text-blue-100 leading-relaxed font-medium z-10 relative">
          Welcome to SmishGuard PH. Cyber defense starts with the community. By reporting a scam, you are practicing modern <b>Bayanihan</b> and protecting millions of Filipinos from fraud.
        </p>
      </div>

      <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-md border border-gray-100 dark:border-slate-700">
        <h3 class="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
          📰 PH Cyber News
        </h3>
        
        <div v-if="newsLoading" class="text-sm text-gray-500 animate-pulse">
          Naglo-load ng balita...
        </div>
        
        <div v-else-if="newsFeed.length === 0" class="text-sm text-gray-500">
          Cannot fetch news at the moment.
        </div>

        <ul v-else class="space-y-4">
          <li v-for="(news, index) in newsFeed" :key="index" class="border-b border-gray-100 dark:border-slate-700 last:border-0 pb-3 last:pb-0">
            <a :href="news.link" target="_blank" rel="noopener noreferrer" class="text-sm font-semibold text-[#0038A8] dark:text-blue-400 hover:underline line-clamp-2">
              {{ news.title }}
            </a>
            <p class="text-xs text-gray-400 mt-1">{{ formatDate(news.pubDate) }}</p>
          </li>
        </ul>
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

      <form @submit.prevent="submitForm" class="space-y-5">
        <div>
          <label class="block mb-1 text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('form.sender_label') }}</label>
          <input v-model="form.sender" type="text" placeholder="e.g. 0917... or GCash" required class="w-full p-3 border border-gray-300 rounded-lg dark:bg-slate-900 dark:border-slate-600 focus:ring-2 focus:ring-[#0038A8] outline-none transition-all">
        </div>
        <div>
          <label class="block mb-1 text-sm font-semibold text-gray-700 dark:text-gray-300">{{ $t('form.message_label') }}</label>
          <textarea v-model="form.message" rows="5" placeholder="Paste the exact scam text message here..." required class="w-full p-3 border border-gray-300 rounded-lg dark:bg-slate-900 dark:border-slate-600 resize-none focus:ring-2 focus:ring-[#0038A8] outline-none transition-all"></textarea>
        </div>
        <button type="submit" :disabled="loading" class="w-full bg-[#0038A8] hover:bg-blue-800 text-white py-4 rounded-lg font-bold text-lg shadow-md transition-all flex justify-center items-center gap-2 disabled:opacity-70">
          <span>{{ loading ? $t('form.processing') : $t('form.submit_btn') }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const form = ref({ sender: '', message: '' });
const loading = ref(false);
const showSuccess = ref(false);

const newsFeed = ref([]);
const newsLoading = ref(true);

const fetchNews = async () => {
  try {
    const res = await fetch('/api/news');
    const data = await res.json();
    if (data.status === 'success') {
      newsFeed.value = data.news;
    }
  } catch (err) {
    console.error("Failed to fetch news", err);
  } finally {
    newsLoading.value = false;
  }
};

const formatDate = (dateString) => {
  const options = { month: 'short', day: 'numeric', year: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

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

onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.4s ease-in-out; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-pulse-slow {
  animation: pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>