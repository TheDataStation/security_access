<template>
    <v-content>
        <v-container fill-height fluid>
            <v-layout align-center justify-center>
                <v-flex md4 sm8 xs12>
                    <v-card class="elevation-12">
                        <v-toolbar color="primary" dark>
                            <v-toolbar-title>{{ appName }}</v-toolbar-title>
                            <v-spacer></v-spacer>
                        </v-toolbar>
                        <v-card-text>
                            <v-form @keyup.enter="submit">
                                <v-text-field v-model="email" label="Login" name="login" prepend-icon="person"
                                              type="text"
                                              @keyup.enter="submit"></v-text-field>
                                <v-text-field id="password" v-model="password" label="Password" name="password"
                                              prepend-icon="lock" type="password" @keyup.enter="submit"></v-text-field>
                            </v-form>
                            <div v-if="loginError">
                                <v-alert :value="loginError" transition="fade-transition" type="error">
                                    Incorrect email or password
                                </v-alert>
                            </div>
                            <v-flex class="caption text-xs-right">
                                <router-link to="/recover-password">Forgot your password?</router-link>
                            </v-flex>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn @click.prevent="submit">Login</v-btn>
                        </v-card-actions>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
</template>

<script lang="ts">
import { appName } from '@/env';
import { dispatchLogIn } from '@/store/actions';
import { readLoginError } from '@/store/getters';
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Login extends Vue {
  public email: string = '';
  public password: string = '';
  public appName = appName;

  public get loginError() {
    return readLoginError(this.$store);
  }

  public submit() {
    dispatchLogIn(this.$store, {
      username: this.email,
      password: this.password,
    });
  }
}
</script>

<style>
</style>
