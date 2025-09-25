<template>
    <Toast />
    <div v-if="loading" class="flex justify-center items-center w-full h-screen">
        <!-- <img src="../../../assets/BienMovieGif.gif" alt="loading" class="w-12rem h-5rem" /> -->
        <ProgressSpinner />
    </div>
    <div v-else class="card p-4">
        <DataTable :value="lists" paginator :rows="10" dataKey="id" v-model:filters="filters" :loading="loading"
            filterDisplay="menu" :globalFilterFields="['name', 'balance']" tableStyle="min-width: 50rem"
            :rowsPerPageOptions="[10, 50, 100, 200, 500, 1000]" :filters="filters"
            paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink  CurrentPageReport "
            currentPageReportTemplate="{totalRecords} şablondan {first} - {last} arası gösteriliyor."
            :scrollable="true">
            <template #header>
                <div class="flex justify-between items-center w-full">
                    <h1 class="text-3xl font-semibold mb-0">Şablonlar</h1>
                    <div class="flex">
                        <Button label="Yeni Şablon Ekle" icon="pi pi-plus" class="mr-4"
                            @click="handleRedirectCreatePage" />
                        <div class="flex justify-content-between flex-column sm:flex-row">
                            <span class="p-input-icon-left">
                                <InputText v-model="filters['global'].value" placeholder="Ara" style="width: 100%" />
                            </span>
                        </div>
                    </div>
                </div>
            </template>
            <template #empty>Şablon bulunamadı.</template>

            <Column field="templateName" header="Şablon Adı" sortable style="width: 5rem" />
            <Column field="createdDate" header="Oluşturulma Tarihi" sortable style="width: 5rem">
                <template #body="{ data }">
                    {{ formatDate(data.createdDate) }}
                </template>
            </Column>
            <Column header="İşlemler" style="width: 5rem" frozen alignFrozen="right">
                <template #body="{ data }">
                    <div class="flex justify-content-center gap-3">
                        <template v-for="item in items" :key="item.label">
                            <Button v-tooltip.top="item.label" :icon="item.icon" rounded size="small"
                                @click="item.command(data)" :severity="item.severity" class="text-white" />
                        </template>
                    </div>
                </template>
            </Column>
        </DataTable>
        <TemplatePreview v-if="selectedTemplate" ref="templatePreviewRef" :template="selectedTemplate"
            :visible="templatePreviewVisible" @closeTemplatePreview="templatePreviewVisible = false" />
    </div>
    <ConfirmDialog></ConfirmDialog>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { FilterMatchMode } from '@primevue/core/api';
import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';
import { useConfirm } from 'primevue/useconfirm';
import { useRouter } from 'vue-router';
import { getTemplates, deleteTemplate } from '@/service/request/user/templateReq';
import { formatDate } from '@/utils/utils';
import TemplatePreview from '@/components/TemplatePreview.vue';
import { useGlobalData } from '@/store/globalData';

const router = useRouter();
const { setSelectedData } = useGlobalData();

const confirm = useConfirm();
const templatePreviewRef = ref(null);

const lists = ref();
const loading = ref(true);
const selectedTemplate = ref(null);
const templatePreviewVisible = ref(false);

const items = ref([
    {
        label: 'Görüntüle',
        icon: 'pi pi-eye',
        severity: 'info',
        command: (data) => {
            selectedTemplate.value = data;
            templatePreviewVisible.value = true;
        }
    },
    {
        label: 'Güncelle',
        icon: 'pi pi-refresh',
        severity: 'success',
        command: (data) => {
            selectedTemplate.value = data;
            setSelectedData(selectedTemplate.value);
            handleRedirectCreatePage();
        }
    },
    {
        label: 'Sil',
        icon: 'pi pi-trash',
        severity: 'danger',
        command: (data) => {
            selectedTemplate.value = data;
            confirmDialog();
        }
    }
]);
const toast = useToast();

const filters = ref({
    global: {
        value: null,
        matchMode: FilterMatchMode.CONTAINS
    }
});

onMounted(async () => {
    setSelectedData(null);
    try {
        const response = await getTemplates();
        lists.value = response?.data?.data.items || [];
        loading.value = false;
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Hata', detail: error?.response?.data?.message || error?.response?.data?.Message, life: 5000 });
    }
});

const handleDeleteTemplate = async () => {
    loading.value = true;
    try {
        await deleteTemplate(selectedTemplate?.value?.id);
        const response = await getTemplates();
        lists.value = response?.data?.data?.items || [];
        toast.add({ severity: 'success', summary: 'Başarılı', detail: 'Şablon başarıyla silindi.', life: 5000 });
    } catch (error) {
        toast.add({ severity: 'error', summary: 'Hata', detail: error?.response?.data?.message || error?.response?.data?.Message, life: 5000 });
    }
    selectedTemplate.value = null;
    loading.value = false;
};

const confirmDialog = () => {
    confirm.require({
        message: 'Bu şablonu silmek istediğinize emin misiniz?',
        header: 'Şablon Silme',
        icon: 'pi pi-info-circle',
        rejectLabel: 'İptal Et',
        acceptLabel: 'Sil',
        rejectClass: 'p-button-secondary p-button-outlined',
        acceptClass: 'p-button-danger ml-2',
        acceptIcon: 'pi pi-trash',
        accept: () => {
            handleDeleteTemplate();
        }
    });
};

const handleRedirectCreatePage = () => {
    router.push({ name: 'templateActions' });
};
</script>
