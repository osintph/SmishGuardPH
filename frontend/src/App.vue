<template>
  <div class="min-h-screen bg-slate-50 text-gray-900 dark:text-gray-100 dark:bg-slate-900 transition-colors pb-10">
    
    <nav class="bg-[#0038A8] dark:bg-slate-800 text-white shadow-md border-b-4 border-[#CE1126] sticky top-0 z-50">
      <div class="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="w-4 h-4 bg-[#FCD116] rounded-full shadow-sm"></div>
          <h1 class="font-extrabold text-lg sm:text-xl tracking-wide">{{ $t('nav.title') }}</h1>
        </div>
        <div class="flex items-center gap-2 sm:gap-4">
          <select v-model="$i18n.locale" class="bg-blue-800 dark:bg-slate-700 rounded px-2 py-1 outline-none text-sm font-semibold cursor-pointer">
            <option value="en">EN</option>
            <option value="fil">FIL</option>
          </select>
          <button @click="toggleDark" class="p-2 bg-blue-800 dark:bg-slate-700 rounded-full text-sm hover:bg-blue-700 transition">
            <span v-if="!isDark">🌙</span><span v-else>☀️</span>
          </button>
        </div>
      </div>
    </nav>

    <div class="max-w-5xl mx-auto px-4 mt-8">
      <ReportScam />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ReportScam from './components/ReportScam.vue';

const isDark = ref(false);

const toggleDark = () => {
  isDark.value = !isDark.value;
  document.documentElement.classList.toggle('dark');
};

onMounted(() => {
  isDark.value = document.documentElement.classList.contains('dark');
});
</script>