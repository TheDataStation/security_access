<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Edit Access Grant</div>
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
                                    <v-select
                                        v-model="decision"
                                        :items="decisions"
                                        box
                                        label="Decision"
                                    ></v-select>
                                    <v-textarea
                                        v-model="decisionReason"
                                        auto-grow
                                        box
                                        label="Decision reason"
                                    ></v-textarea>
                                </template>
                                <v-date-picker v-model="expiry" @input="menu = false"></v-date-picker>
                            </v-menu>
                        </v-flex>
                        <v-switch
                            v-model="revealSharer"
                            label="Reveal sharer"
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
import { IAccessDecision, IAccessUpdate, IQueryType } from '@/interfaces';
import {
  dispatchGetAccesses,
  dispatchUpdateAccessGrant,
} from '@/store/actions';
import { readOneAccessGrant } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class EditAccessGrant extends Vue {
  public menu = false;
  public loading = false;
  public expiry: string | number = '';
  public revealSharer = false;
  public decision: IAccessDecision = IAccessDecision.IPending;
  public decisionReason: string = '';
  public decisions = Object.keys(IAccessDecision).map((k) =>
    IAccessDecision[k as any].toUpperCase(),
  );

  get accessGrant() {
    return readOneAccessGrant(this.$store)(
      +this.$router.currentRoute.params.id,
    );
  }

  public async mounted() {
    await dispatchGetAccesses(this.$store);
    this.reset();
  }

  public reset() {
    this.expiry = '';
    this.revealSharer = false;
    if (this.accessGrant) {
      this.expiry = this.accessGrant.expiry ? this.accessGrant.expiry : '';
      this.revealSharer = this.accessGrant.reveal_sharer
        ? this.accessGrant.reveal_sharer
        : false;
      this.decision = this.accessGrant.decision
        ? this.accessGrant.decision
        : IAccessDecision.IMaybe;
      this.decisionReason = this.accessGrant.decision_reason
        ? this.accessGrant.decision_reason
        : '';
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    const updatedAccessGrant: IAccessUpdate = {};
    if (this.expiry) {
      updatedAccessGrant.expiry = this.expiry;
    }
    if (this.revealSharer) {
      updatedAccessGrant.reveal_sharer = this.revealSharer;
    }
    if (this.decisionReason) {
      updatedAccessGrant.decision_reason = this.decisionReason;
    }
    await dispatchUpdateAccessGrant(this.$store, {
      id: this.accessGrant!.id,
      query: updatedAccessGrant,
    });
    this.$router.push('/main/accesses');
  }
}
</script>
