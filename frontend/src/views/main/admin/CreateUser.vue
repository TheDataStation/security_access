<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Create User</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-form ref="form" v-model="valid" lazy-validation>
                        <v-text-field v-model="fullName" label="Full Name" required></v-text-field>
                        <v-text-field v-model="email" v-validate="'required|email'"
                                      :error-messages="errors.collect('email')" data-vv-name="email" label="E-mail"
                                      required type="email"></v-text-field>
                        <div class="subheading secondary--text text--lighten-2">User is superuser <span
                            v-if="isSuperuser">(currently is a superuser)</span><span
                            v-else>(currently is not a superuser)</span></div>
                        <v-checkbox v-model="isSuperuser" label="Is Superuser"></v-checkbox>
                        <div class="subheading secondary--text text--lighten-2">User is active <span v-if="isActive">(currently active)</span><span
                            v-else>(currently not active)</span></div>
                        <v-checkbox v-model="isActive" label="Is Active"></v-checkbox>
                        <v-layout align-center>
                            <v-flex>
                                <v-text-field ref="password" v-model="password1" v-validate="{required: true}"
                                              :error-messages="errors.first('password')"
                                              data-vv-delay="100" data-vv-name="password" label="Set Password"
                                              type="password">
                                </v-text-field>
                                <v-text-field v-model="password2" v-validate="{required: true, confirmed: 'password'}"
                                              :error-messages="errors.first('password_confirmation')"
                                              data-vv-as="password" data-vv-delay="100"
                                              data-vv-name="password_confirmation" label="Confirm Password"
                                              type="password">
                                </v-text-field>
                            </v-flex>
                        </v-layout>
                    </v-form>
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Cancel</v-btn>
                <v-btn @click="reset">Reset</v-btn>
                <v-btn :disabled="!valid" @click="submit">
                    Save
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {IUserProfileCreate} from '@/interfaces';
import {dispatchCreateUser, dispatchGetUsers} from '@/store/admin/actions';

@Component
export default class CreateUser extends Vue {
    public valid = false;
    public fullName: string = '';
    public email: string = '';
    public isActive: boolean = true;
    public isSuperuser: boolean = false;
    public setPassword = false;
    public password1: string = '';
    public password2: string = '';

    public async mounted() {
        await dispatchGetUsers(this.$store);
        this.reset();
    }

    public reset() {
        this.password1 = '';
        this.password2 = '';
        this.fullName = '';
        this.email = '';
        this.isActive = true;
        this.isSuperuser = false;
        this.$validator.reset();
    }

    public cancel() {
        this.$router.back();
    }

    public async submit() {
        if (await this.$validator.validateAll()) {
            const updatedProfile: IUserProfileCreate = {
                email: this.email,
            };
            if (this.fullName) {
                updatedProfile.full_name = this.fullName;
            }
            if (this.email) {
                updatedProfile.email = this.email;
            }
            updatedProfile.is_active = this.isActive;
            updatedProfile.is_superuser = this.isSuperuser;
            updatedProfile.password = this.password1;
            await dispatchCreateUser(this.$store, updatedProfile);
            this.$router.push('/main/admin/users');
        }
    }
}
</script>
