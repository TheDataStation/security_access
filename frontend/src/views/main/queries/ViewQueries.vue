<template>
    <div>
        <v-toolbar light>
            <v-toolbar-title>
                Manage Queries
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn :to="{name: 'main-queries-create'}" color="primary">Create Query</v-btn>
        </v-toolbar>
        <v-data-table :headers="queryHeaders" :items="queries">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td>{{ props.item.type }}</td>
                <td>{{ props.item.description }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>View</span>
                        <v-btn slot="activator" :to="{name: 'main-queries-view', params: {id: props.item.id}}"
                               flat>
                            <v-icon>search</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
        <p></p>
        <v-toolbar light>
            <v-toolbar-title>
                Manage Query Requests
            </v-toolbar-title>
        </v-toolbar>
        <v-data-table :headers="queryRequestHeaders" :items="queryRequests">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td v-if="props.item.expiry">{{ props.item.expiry | dateParse('YYYY-MM-DDTHH:mm') | dateFormat('YYYY-MM-DD') }}</td>
                <td v-else>Never</td>
                <td>{{ props.item.reveal_input_data ? '✅' : '❌' }}</td>
                <td>{{ props.item.reveal_querier ? '✅' : '❌' }}</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Edit</span>
                        <v-btn slot="activator" :to="{name: 'main-queries-requests-edit', params: {id: props.item.id}}"
                               flat>
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
import {readQueries, readQueryRequests} from '@/store/getters';
import {dispatchGetQueries, dispatchGetQueryRequests} from '@/store/actions';

@Component
export default class Queries extends Vue {
    public queryHeaders = [
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
            text: 'Type',
            sortable: true,
            value: 'type',
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

    public queryRequestHeaders = [
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
            text: 'Expiry',
            sortable: true,
            value: 'expiry',
            align: 'left',
        },
        {
            text: 'Reveal input data',
            sortable: true,
            value: 'reveal_input_data',
            align: 'left',
        },
        {
            text: 'Reveal querier',
            sortable: true,
            value: 'reveal_querier',
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

    get queryRequests() {
        return readQueryRequests(this.$store);
    }

    public async mounted() {
        await dispatchGetQueries(this.$store);
        await dispatchGetQueryRequests(this.$store);
    }
}
</script>
