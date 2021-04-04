<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Create Query</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-textarea
                        v-model="description"
                        auto-grow
                        box
                        disabled
                        label="Description"
                    ></v-textarea>
                    <v-textarea
                        v-model="payload"
                        auto-grow
                        box
                        disabled
                        label="Payload"
                    ></v-textarea>
                    <v-text-field
                        v-model="type"
                        box
                        disabled
                        label="Query type"
                    ></v-text-field>
                    <!--                        <div class="subheading secondary&#45;&#45;text text&#45;&#45;lighten-2">Files</div>-->
                    <!--                        <v-divider></v-divider>-->
                    <!--                        <p></p>-->
                    <!--                        <file-pond-->
                    <!--                            ref="pond"-->
                    <!--                            :allow-multiple="true"-->
                    <!--                            accepted-file-types="image/jpeg, image/png"-->
                    <!--                            label-idle="Drop files here..."-->
                    <!--                            name="file"-->
                    <!--                            v-on:init="handleFilePondInit"-->
                    <!--                            v-on:processfile="handleFilePondUploadFile"-->
                    <!--                        />-->
                </template>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn @click="cancel">Back</v-btn>
                <!--                <v-btn @click="reset">Reset</v-btn>-->
                <!--                <v-btn-->
                <!--                    :disabled="!valid"-->
                <!--                    @click="submit"-->
                <!--                >-->
                <!--                    Save-->
                <!--                </v-btn>-->
            </v-card-actions>
        </v-card>
    </v-container>
</template>

<script lang="ts">
import {Component, Vue} from 'vue-property-decorator';
import {dispatchGetQueries} from '@/store/actions';
import {readOneQuery} from '@/store/getters';
import {IQueryType} from '@/interfaces';

@Component
export default class ViewQuery extends Vue {
    public description?: string = '';
    public type: IQueryType = IQueryType.IOther;
    public fileIds: any[] = [];
    public payload: string = '';

    public async mounted() {
        await dispatchGetQueries(this.$store);
        const query = readOneQuery(this.$store)(+this.$router.currentRoute.params.id);
        this.payload = JSON.stringify(query!.payload, null, 8).replaceAll('"', '');
        this.description = query!.description;
        this.type = query!.type!;
    }

    public cancel() {
        this.$router.back();
    }
}
</script>
