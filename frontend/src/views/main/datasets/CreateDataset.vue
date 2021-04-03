<template>
    <v-container fluid>
        <v-card class="ma-3 pa-3">
            <v-card-title primary-title>
                <div class="headline primary--text">Create Dataset</div>
            </v-card-title>
            <v-card-text>
                <template>
                    <v-form
                        ref="form"
                        v-model="valid"
                        lazy-validation
                    >
                        <v-text-field
                            v-model="title"
                            label="Title"
                            required
                            box
                        ></v-text-field>
                        <v-textarea
                            v-model="description"
                            auto-grow
                            label="Description"
                            box
                        ></v-textarea>
                        <div class="subheading secondary--text text--lighten-2">Files</div>
                        <v-divider></v-divider>
                        <p></p>
                        <file-pond
                            ref="pond"
                            :allow-multiple="true"
                            accepted-file-types="image/jpeg, image/png"
                            label-idle="Drop files here..."
                            name="file"
                            v-on:init="handleFilePondInit"
                            v-on:processfile="handleFilePondUploadFile"
                        />
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
import {Component, Vue} from 'vue-property-decorator';
import {dispatchCreateDataset, dispatchGetDatasets} from '@/store/actions';

// Import Vue FilePond
import VueFilePond from 'vue-filepond';
import {setOptions} from 'filepond';
// Import FilePond styles
import 'filepond/dist/filepond.min.css';
import {api} from '@/api';
import {readToken} from '@/store/getters';
import {store} from '@/store';
import {IDatasetCreate} from '@/interfaces';


const FilePond = VueFilePond();


@Component({
    components: {
        FilePond,
    },
})
export default class CreateDataset extends Vue {
    public valid = true;
    public loading = false;
    public title: string = '';
    public description?: string = '';
    public fileIds: any[] = [];

    public handleFilePondInit() {
        // FilePond instance methods are available on `this.$refs.pond`
        // console.log(this.$refs.pond);
    }

    public handleFilePondUploadFile(err, file) {
        this.fileIds.push(parseInt(file.serverId, 10));
    }

    public async mounted() {
        setOptions({
            server: {
                url: api.uploadUrl,
                ...api.authHeaders(readToken(store)),
            },
        });
        await dispatchGetDatasets(this.$store);

        this.reset();
    }

    public reset() {
        this.title = '';
        this.description = '';
        this.fileIds = [];
        this.loading = false;
        this.$validator.reset();
    }

    public cancel() {
        this.$router.back();
    }

    public async submit() {
        if (await this.$validator.validateAll()) {
            const createdDataset: IDatasetCreate = {
                title: this.title,
                description: '',
                file_ids: this.fileIds,
            };
            if (this.description) {
                createdDataset.description = this.description;
            }
            // TODO(max): on failure files don't get deleted server side
            await dispatchCreateDataset(this.$store, createdDataset);
            await this.$router.push('/main/datasets');

        }
    }
}
</script>

