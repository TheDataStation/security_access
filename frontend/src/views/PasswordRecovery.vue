<template>
    <v-content>
        <v-container fill-height fluid>
            <v-layout align-center justify-center>
                <v-flex md4 sm8 xs12>
                    <v-card class="elevation-12">
                        <v-toolbar color="primary" dark>
                            <v-toolbar-title>{{ appName }} - Password Recovery</v-toolbar-title>
                        </v-toolbar>
                        <v-card-text>
                            <p class="subheading">A password recovery email will be sent to the registered account</p>
                            <v-form ref="form" v-model="valid" lazy-validation @keyup.enter="submit" @submit.prevent="">
                                <v-text-field v-model="username" v-validate="'required'"
                                              :error-messages="errors.collect('username')" data-vv-name="username"
                                              label="Username" prepend-icon="person" required
                                              type="text" @keyup.enter="submit"></v-text-field>
                            </v-form>
                        </v-card-text>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <v-btn @click="cancel">Cancel</v-btn>
                            <v-btn :disabled="!valid" @click.prevent="submit">
                                Recover Password
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </v-content>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {appName} from '@/env';
import {dispatchPasswordRecovery} from '@/store/main/actions';

@Component
export default class Login extends Vue {
    public valid = true;
    public username: string = '';
    public appName = appName;

    public cancel() {
        this.$router.back();
    }

    public submit() {
        dispatchPasswordRecovery(this.$store, {username: this.username});
    }
}
</script>

<style>
</style>
