<template>
    <div>
        <v-toolbar light>
            <v-toolbar-title>
                Manage Queries
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn :to="{name: 'main-queries-create'}" color="primary">Create Query</v-btn>
        </v-toolbar>
        <v-data-table :headers="headers" :items="queries">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td>{{ props.item.payload }}</td>
                <td>{{ props.item.description }}</td>
<!--                <td>{{ props.item.file_ids }}</td>-->
                <!--                <td class="justify-center layout px-0">-->
                <!--                    <v-tooltip top>-->
                <!--                        <span>Edit</span>-->
                <!--                        <v-btn slot="activator" :to="{name: 'main-queries-edit', params: {id: props.item.id}}" flat>-->
                <!--                            <v-icon>edit</v-icon>-->
                <!--                        </v-btn>-->
                <!--                    </v-tooltip>-->
                <!--                </td>-->
            </template>
        </v-data-table>
    </div>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {readQueries} from '@/store/getters';
import {dispatchGetQueries} from '@/store/actions';

@Component
export default class Queries extends Vue {
    public headers = [
        {
            text: 'id',
            sortable: true,
            value: 'id',
            align: 'left',
        },
        {
            text: 'Created at',
            sortable: true,
            value: 'created_at',
            align: 'left',
        },
        {
            text: 'Payload',
            sortable: true,
            value: 'payload',
            align: 'left',
        },
        {
            text: 'Description',
            sortable: true,
            value: 'description',
            align: 'left',
        },
        // {
        //     text: 'File IDs',
        //     sortable: true,
        //     value: 'file_ids',
        //     align: 'left',
        // },
    ];

    get queries() {
        return readQueries(this.$store);
    }

    public async mounted() {
        await dispatchGetQueries(this.$store);
    }
}
</script>
