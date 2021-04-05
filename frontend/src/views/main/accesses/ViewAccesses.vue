<template>
    <div>
        <v-toolbar light>
            <v-toolbar-title>
                Access Grants
            </v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-data-table :headers="headers" :items="accessGrants">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td>{{ props.item.decision }}</td>
                <td>{{ props.item.reveal_sharer ? '✅' : '❌' }}</td>
                <td>{{ props.item.decision_reason }}</td>
                <td v-if="props.item.expiry">{{ props.item.expiry | dateParse('YYYY-MM-DDTHH:mm') | dateFormat('YYYY-MM-DD') }}</td>
                <td v-else>Never</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Edit</span>
                        <v-btn slot="activator" :to="{name: 'main-accesses-edit', params: {id: props.item.id}}" flat>
                            <v-icon>edit</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
        <p></p>
        <v-toolbar light>
            <v-toolbar-title>
                Access Receipts
            </v-toolbar-title>
            <v-spacer></v-spacer>
        </v-toolbar>
        <v-data-table :headers="headers" :items="accessReceipts">
            <template slot="items" slot-scope="props">
                <td>{{ props.item.id }}</td>
                <td>{{ props.item.created_at | dateParse('YYYY-MM-DDTHH:mm:ss') | dateFormat('YYYY-MM-DD') }}</td>
                <td>{{ props.item.decision }}</td>
                <td>{{ props.item.reveal_sharer ? '✅' : '❌' }}</td>
                <td>{{ props.item.decision_reason }}</td>
                <td v-if="props.item.expiry">{{ props.item.expiry | dateParse('YYYY-MM-DDTHH:mm') | dateFormat('YYYY-MM-DD') }}</td>
                <td v-else>Never</td>
                <td class="justify-center layout px-0">
                    <v-tooltip top>
                        <span>Edit</span>
                        <v-btn slot="activator" :to="{name: 'main-accesses-view', params: {id: props.item.id}}" flat>
                            <v-icon>search</v-icon>
                        </v-btn>
                    </v-tooltip>
                </td>
            </template>
        </v-data-table>
    </div>
</template>

<script lang="ts">
import { dispatchGetAccesses } from '@/store/actions';
import { readAccessGrants, readAccessReceipts } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Accesses extends Vue {
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
      text: 'Decision',
      sortable: true,
      value: 'decision',
      align: 'left',
    },
    {
      text: 'Reveal sharer',
      sortable: true,
      value: 'reveal_sharer',
      align: 'left',
    },
    {
      text: 'Decision reason',
      sortable: true,
      value: 'decision_reason',
      align: 'left',
    },
    {
      text: 'Expiry',
      sortable: true,
      value: 'expiry',
      align: 'left',
    },
  ];

  get accessGrants() {
    return readAccessGrants(this.$store);
  }
  get accessReceipts() {
    return readAccessReceipts(this.$store);
  }

  public async mounted() {
    await dispatchGetAccesses(this.$store);
  }
}
</script>
