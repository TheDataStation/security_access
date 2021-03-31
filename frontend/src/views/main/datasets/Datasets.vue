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
                <td>{{ props.item.name }}</td>
                <td>{{ props.item.email }}</td>
                <td>{{ props.item.full_name }}</td>
<!--                <td>-->
<!--                    <v-icon v-if="props.item.is_active">checkmark</v-icon>-->
<!--                </td>-->
<!--                <td>-->
<!--                    <v-icon v-if="props.item.is_superdataset">checkmark</v-icon>-->
<!--                </td>-->
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
            text: 'Name',
            sortable: true,
            value: 'name',
            align: 'left',
        },
        {
            text: 'Email',
            sortable: true,
            value: 'email',
            align: 'left',
        },
        {
            text: 'Full Name',
            sortable: true,
            value: 'full_name',
            align: 'left',
        },
        {
            text: 'Is Active',
            sortable: true,
            value: 'isActive',
            align: 'left',
        },
        {
            text: 'Is Superdataset',
            sortable: true,
            value: 'isSuperdataset',
            align: 'left',
        },
        {
            text: 'Actions',
            value: 'id',
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
