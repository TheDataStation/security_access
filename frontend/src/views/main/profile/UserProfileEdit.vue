<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Edit User Profile</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-form
                        ref="form"
                        v-model="valid"
                        lazy-validation
                    >
                        <v-text-field
                            v-model="fullName"
                            label="Full Name"
                            required
                        ></v-text-field>
                        <v-text-field
                            v-model="email"
                            v-validate="'required|email'"
                            :error-messages="errors.collect('email')"
                            data-vv-name="email"
                            label="E-mail"
                            required
                            type="email"
                        ></v-text-field>
                    </v-form>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Cancel</v-btn>
                <v-btn @click="reset">Reset</v-btn>
                <v-btn
                    :disabled="!valid"
                    @click="submit"
                >
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import { IUserUpdate } from '@/interfaces';
import { dispatchUpdateUserProfile } from '@/store/actions';
import { readUserProfile } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class UserProfileEdit extends Vue {
  public valid = true;
  public fullName: string = '';
  public email: string = '';

  get userProfile() {
    return readUserProfile(this.$store);
  }

  public created() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      this.fullName = userProfile.full_name!;
      this.email = userProfile.email!;
    }
  }

  public reset() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      this.fullName = userProfile.full_name!;
      this.email = userProfile.email!;
    }
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if ((this.$refs.form as any).validate()) {
      const updatedProfile: IUserUpdate = {};
      if (this.fullName) {
        updatedProfile.full_name = this.fullName;
      }
      if (this.email) {
        updatedProfile.email = this.email;
      }
      await dispatchUpdateUserProfile(this.$store, updatedProfile);
      await this.$router.push('/main/profile');
    }
  }
}
</script>
