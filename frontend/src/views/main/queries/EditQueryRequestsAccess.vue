<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Edit Query Request</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-form
                        ref="form"
                    >
                        <v-flex md4 sm6 xs12>
                            <v-menu
                                v-model="menu"
                                :close-on-content-click="true"
                                :nudge-right="40"
                                full-width
                                lazy
                                min-width="290px"
                                offset-y
                                transition="scale-transition"
                            >
                                <template v-slot:activator="{ on }">
                                    <v-text-field
                                        v-model="expiry"
                                        v-on="on"
                                        label="Expiry date"
                                        prepend-icon="event"
                                        readonly
                                    ></v-text-field>
                                </template>
                                <v-date-picker v-model="expiry" @input="menu = false"></v-date-picker>
                            </v-menu>
                        </v-flex>
                        <v-switch
                            v-model="revealInputData"
                            label="Reveal input data"
                        ></v-switch>
                        <v-switch
                            v-model="revealQuerier"
                            label="Reveal querier"
                        ></v-switch>
                    </v-form>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn v-on:click="cancel">Cancel</v-btn>
                <v-btn v-on:click="reset">Reset</v-btn>
                <v-btn v-on:click="submit">Save</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import { IQueryRequestsAccessUpdate } from '@/interfaces';
import {
  dispatchGetQueryRequests,
  dispatchUpdateQueryRequests,
} from '@/store/actions';
import { readOneQueryRequest } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class EditQueryRequestsAccess extends Vue {
  public menu = false;
  public loading = false;
  public createdAt = '';
  public expiry: string | number = '';
  public revealInputData = false;
  public revealQuerier = false;

  get queryRequestsAccess() {
    return readOneQueryRequest(this.$store)(
      +this.$router.currentRoute.params.id,
    );
  }

  public async mounted() {
    await dispatchGetQueryRequests(this.$store);
    this.reset();
  }

  public reset() {
    this.createdAt = '';
    this.expiry = '';
    this.revealInputData = false;
    this.revealQuerier = false;
    if (this.queryRequestsAccess) {
      this.createdAt = this.queryRequestsAccess.created_at;
      this.expiry = this.queryRequestsAccess.expiry
        ? this.queryRequestsAccess.expiry
        : '';
      this.revealInputData = this.queryRequestsAccess.reveal_input_data
        ? this.queryRequestsAccess.reveal_input_data
        : false;
      this.revealQuerier = this.queryRequestsAccess.reveal_querier
        ? this.queryRequestsAccess.reveal_querier
        : false;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    const updatedQueryRequest: IQueryRequestsAccessUpdate = {};
    if (this.expiry) {
      updatedQueryRequest.expiry = this.expiry;
    }
    if (this.revealInputData) {
      updatedQueryRequest.reveal_input_data = this.revealInputData;
    }
    if (this.revealQuerier) {
      updatedQueryRequest.reveal_querier = this.revealQuerier;
    }
    await dispatchUpdateQueryRequests(this.$store, {
      id: this.queryRequestsAccess!.id,
      query: updatedQueryRequest,
    });
    this.$router.push('/main/queryRequests');
  }
}
</script>
