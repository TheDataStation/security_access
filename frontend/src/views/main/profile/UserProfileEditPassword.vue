<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Set Password</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <div class="my-3">
                        <div class="subheading secondary--text text--lighten-2">User</div>
                        <div v-if="userProfile.full_name" class="title primary--text text--darken-2">
                            {{ userProfile.full_name }}
                        </div>
                        <div v-else class="title primary--text text--darken-2">{{ userProfile.email }}</div>
                    </div>
                    <v-form ref="form">
                        <v-text-field
                            ref="password"
                            v-model="password1"
                            v-validate="'required'"
                            :error-messages="errors.first('password')"
                            data-vv-delay="100"
                            data-vv-name="password"
                            data-vv-rules="required"
                            label="Password"
                            type="password">
                        </v-text-field>
                        <v-text-field
                            v-model="password2"
                            v-validate="'required|confirmed:password'"
                            :error-messages="errors.first('password_confirmation')"
                            data-vv-as="password"
                            data-vv-delay="100"
                            data-vv-name="password_confirmation"
                            data-vv-rules="required|confirmed:$password"
                            label="Confirm Password"
                            type="password">
                        </v-text-field>
                    </v-form>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Cancel</v-btn>
                <v-btn @click="reset">Reset</v-btn>
                <v-btn :disabled="!valid" @click="submit">Save</v-btn>
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
  public password1 = '';
  public password2 = '';

  get userProfile() {
    return readUserProfile(this.$store);
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.back();
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const updatedProfile: IUserUpdate = {};
      updatedProfile.password = this.password1;
      await dispatchUpdateUserProfile(this.$store, updatedProfile);
      await this.$router.push('/main/profile');
    }
  }
}
</script>
