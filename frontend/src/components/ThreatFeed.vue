<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-gray-100 dark:border-slate-700 p-6 sm:p-8 overflow-hidden">
    <h2 class="text-2xl font-extrabold mb-2 text-[#CE1126] dark:text-red-400">{{ $t('feed.title') }}</h2>
    <p class="text-gray-600 dark:text-gray-400 mb-6 text-sm">{{ $t('feed.desc') }}</p>

    <div class="overflow-x-auto rounded-lg border border-gray-200 dark:border-slate-700">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="bg-gray-50 dark:bg-slate-700 border-b border-gray-200 dark:border-slate-600">
            <th class="p-3 text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('feed.col_date') }}</th>
            <th class="p-3 text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('feed.col_sender') }}</th>
            <th class="p-3 text-sm font-bold text-gray-700 dark:text-gray-300">{{ $t('feed.col_url') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading" class="border-b dark:border-slate-700">
            <td colspan="3" class="p-6 text-center text-gray-500 font-medium animate-pulse">Fetching latest threats...</td>
          </tr>
          <tr v-else-if="feed.length === 0" class="border-b dark:border-slate-700">
             <td colspan="3" class="p-6 text-center text-gray-500 font-medium">{{ $t('feed.empty') }}</td>
          </tr>
          <tr v-else v-for="item in feed" :key="item.id" class="border-b border-gray-100 dark:border-slate-700 hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors">
            <td class="p-3 text-sm text-gray-600 dark:text-gray-400 whitespace-nowrap">{{ formatDate(item.timestamp) }}</td>
            <td class="p-3 text-sm font-medium text-gray-900 dark:text-gray-200">{{ item.sender }}</td>
            <td class="p-3 text-sm">
              <span v-if="item.extracted_url === 'No URL detected'" class="text-gray-400 italic">{{ item.extracted_url }}</span>
              <span v-else class="text-[#CE1126] dark:text-red-400 font-bold break-all">{{ item.extracted_url }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const feed = ref([]);
const loading = ref(true);

const fetchFeed = async () => {
  try {
    const res = await fetch('/api/feed');
    const data = await res.json();
    feed.value = data.threat_feed;
  } catch (err) {
    console.error("Failed to fetch feed:", err);
  } finally {
    loading.value = false;
  }
};

const formatDate = (isoString) => {
  const date = new Date(isoString);
  return date.toLocaleString(); // Formats automatically to the user's local time
};

onMounted(() => {
  fetchFeed();
});
</script>