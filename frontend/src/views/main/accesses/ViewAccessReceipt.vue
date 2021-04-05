<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">View Access</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-text-field
                        v-model="expiry"
                        label="Expiry date"
                        prepend-icon="event"
                        disabled
                    ></v-text-field>
                    <v-text-field
                        v-model="decision"
                        label="Decision"
                        disabled
                    ></v-text-field>
                    <v-textarea
                        v-model="decisionReason"
                        auto-grow
                        box
                        disabled
                        label="Decision reason"
                    ></v-textarea>
                    <v-switch
                        v-model="revealSharer"
                        label="Reveal sharer"
                        disabled
                    ></v-switch>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Back</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import { dispatchGetAccesses } from '@/store/actions';
import { readOneAccessReceipt } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class ViewAccessReceipt extends Vue {
  public decision?: string = '';
  public expiry: string | number = '';
  public decisionReason?: string = '';
  public revealSharer?: boolean = false;

  public async mounted() {
    await dispatchGetAccesses(this.$store);
    const access = readOneAccessReceipt(this.$store)(
      +this.$router.currentRoute.params.id,
    );
    this.decision = access!.decision;
    this.expiry = access!.expiry ? access!.expiry : 'NEVER';
    this.decisionReason = access!.decision_reason
      ? access!.decision_reason.toUpperCase()
      : '';
    this.revealSharer = access!.reveal_sharer;
  }

  public cancel() {
    this.$router.back();
  }
}
</script>
