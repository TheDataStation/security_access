<template>
    <div>
        <v-toolbar light>
            <v-toolbar-title>
                Manage Datasets
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn color="primary" to="/main/datasets/create">Create Dataset</v-btn>
        </v-toolbar>
        <v-data-table :headers="headers" :items="datasets">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td>{{ props.item.title }}</td>
                <td>{{ props.item.description }}</td>
                <td>{{ props.item.url_ids }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Edit</span>
                        <v-btn slot="activator" :to="{name: 'main-datasets-edit', params: {id: props.item.id}}" flat>
                            <v-icon>edit</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readDatasets} from '@/store/main/getters';
import {dispatchGetDatasets} from '@/store/main/actions';

@Component
export default class Datasets extends Vue {
    public headers = [
        {
            text: 'Created at',
            sortable: true,
            value: 'created_at',
            align: 'left',
        },
        {
            text: 'Title',
            sortable: true,
            value: 'title',
            align: 'left',
        },
        {
            text: 'Description',
            sortable: true,
            value: 'description',
            align: 'left',
        },
        {
            text: 'URL IDs',
            sortable: true,
            value: 'url_ids',
            align: 'left',
        },
    ];

    get datasets() {
        return readDatasets(this.$store);
    }

    public async mounted() {
        await dispatchGetDatasets(this.$store);
    }
}
</script>
