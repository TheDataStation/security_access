<template>
    <v-content>
        <v-container fill-height fluid>
            <v-layout align-center justify-center>
                <v-flex md4 sm8 xs12>
                    <v-card class="elevation-12">
                        <v-toolbar color="primary" dark>
                            <v-toolbar-title>{{ appName }} - Reset Password</v-toolbar-title>
                        </v-toolbar>
                        <v-card-text>
                            <p class="subheading">Enter your new password below</p>
                            <v-form ref="form" v-model="valid" lazy-validation @keyup.enter="submit" @submit.prevent="">
                                <v-text-field ref="password" v-model="password1" v-validate="'required'"
                                              :error-messages="errors.first('password')"
                                              data-vv-delay="100" data-vv-name="password" data-vv-rules="required"
                                              label="Password"
                                              type="password">
                                </v-text-field>
                                <v-text-field v-model="password2" v-validate="'required|confirmed:password'"
                                              :error-messages="errors.first('password_confirmation')"
                                              data-vv-as="password" data-vv-delay="100"
                                              data-vv-name="password_confirmation"
                                              data-vv-rules="required|confirmed:$password" label="Confirm Password"
                                              type="password">
                                </v-text-field>
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn @click="cancel">Cancel</v-btn>
                            <v-btn @click="reset">Clear</v-btn>
                            <v-btn :disabled="!valid" @click="submit">Save</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
</template>

<script lang="ts">
import { appName } from '@/env';
import { dispatchResetPassword } from '@/store/actions';
import { commitAddNotification } from '@/store/mutations';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class UserProfileEdit extends Vue {
  public appName = appName;
  public valid = true;
  public password1 = '';
  public password2 = '';

  public mounted() {
    this.checkToken();
  }

  public reset() {
    this.password1 = '';
    this.password2 = '';
    this.$validator.reset();
  }

  public cancel() {
    this.$router.push('/');
  }

  public checkToken() {
    const token = this.$router.currentRoute.query.token as string;
    if (!token) {
      commitAddNotification(this.$store, {
        content: 'No token provided in the URL, start a new password recovery',
        color: 'error',
      });
      this.$router.push('/recover-password');
    } else {
      return token;
    }
  }

  public async submit() {
    if (await this.$validator.validateAll()) {
      const token = this.checkToken();
      if (token) {
        await dispatchResetPassword(this.$store, {
          token,
          password: this.password1,
        });
        await this.$router.push('/');
      }
    }
  }
}
</script>
