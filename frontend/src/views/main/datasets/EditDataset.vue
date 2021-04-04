<!--<template>-->
<!--    <v-container fluid>-->
<!--        <v-card class="ma-3 pa-3">-->
<!--            <v-card-title primary-title>-->
<!--                <div class="headline primary&#45;&#45;text">Edit Dataset</div>-->
<!--            </v-card-title>-->
<!--            <v-card-text>-->
<!--                <template>-->
<!--                    <div class="my-3">-->
<!--                        <div class="subheading secondary&#45;&#45;text text&#45;&#45;lighten-2">Dataset title</div>-->
<!--                        <div-->
<!--                            v-if="dataset"-->
<!--                            class="title primary&#45;&#45;text text&#45;&#45;darken-2"-->
<!--                        >{{ dataset.title }}-->
<!--                        </div>-->
<!--                        <div-->
<!--                            v-else-->
<!--                            class="title primary&#45;&#45;text text&#45;&#45;darken-2"-->
<!--                        >-&#45;&#45;&#45;&#45;-->
<!--                        </div>-->
<!--                    </div>-->
<!--                    <v-form-->
<!--                        ref="form"-->
<!--                        v-model="valid"-->
<!--                        lazy-validation-->
<!--                    >-->
<!--                        <v-text-field-->
<!--                            v-model="title"-->
<!--                            label="Full Name"-->
<!--                            required-->
<!--                        ></v-text-field>-->
<!--                        <v-text-field-->
<!--                            v-model="description"-->
<!--                            v-validate="'required'"-->
<!--                            :error-messages="errors.collect('description')"-->
<!--                            data-vv-name="description"-->
<!--                            label="Description"-->
<!--                            required-->
<!--                        ></v-text-field>-->
<!--                        <div class="subheading secondary&#45;&#45;text text&#45;&#45;lighten-2">Files</div>-->
<!--                        <v-divider></v-divider>-->
<!--                        <p></p>-->
<!--                        <vue-dropzone id="dropzone" ref="myVueDropzone" :options="dropzoneOptions"></vue-dropzone>-->
<!--                    </v-form>-->
<!--                </template>-->
<!--            </v-card-text>-->
<!--            <v-card-actions>-->
<!--                <v-spacer></v-spacer>-->
<!--                <v-btn @click="cancel">Cancel</v-btn>-->
<!--                <v-btn @click="reset">Reset</v-btn>-->
<!--                <v-btn-->
<!--                    :disabled="!valid"-->
<!--                    @click="submit"-->
<!--                >-->
<!--                    Save-->
<!--                </v-btn>-->
<!--            </v-card-actions>-->
<!--        </v-card>-->
<!--    </v-container>-->
<!--</template>-->

<!--<script lang="ts">-->
<!--import {Component, Vue} from 'vue-property-decorator';-->
<!--import {IDatasetUpdate} from '@/interfaces';-->
<!--import {dispatchGetDatasets, dispatchUpdateDataset} from '@/store/actions';-->
<!--import {readOneDataset} from '@/store/getters';-->


<!--// Import Vue FilePond-->
<!--import VueFilePond from 'vue-filepond';-->
<!--// Import FilePond styles-->
<!--import 'filepond/dist/filepond.min.css';-->
<!--import vue2Dropzone from 'vue2-dropzone'-->
<!--import 'vue2-dropzone/dist/vue2Dropzone.min.css'-->

<!--const FilePond = VueFilePond();-->

<!--@Component({-->
<!--    components: {-->
<!--        FilePond,-->
<!--        vueDropzone: vue2Dropzone-->
<!--    },-->
<!--})-->
<!--export default class EditDataset extends Vue {-->
<!--    public valid = true;-->
<!--    public loading = false;-->
<!--    public title: string = '';-->
<!--    public fileName: string = '';-->
<!--    public description?: string = '';-->
<!--    public data: string[] = [];-->
<!--    public myFiles = [];-->
<!--    public dropzoneOptions = {-->
<!--        url: 'https://httpbin.org/post',-->
<!--        thumbnailWidth: 150,-->
<!--        maxFilesize: 0.5,-->
<!--        headers: {"My-Awesome-Header": "header value"},-->
<!--        autoProcessQueue: false,-->
<!--    };-->


<!--    get dataset() {-->
<!--        return readOneDataset(this.$store)(+this.$router.currentRoute.params.id);-->
<!--    }-->

<!--    public async mounted() {-->
<!--        await dispatchGetDatasets(this.$store);-->
<!--        this.reset();-->
<!--    }-->

<!--    public reset() {-->
<!--        this.title = '';-->
<!--        this.description = '';-->
<!--        this.data = [];-->
<!--        this.$validator.reset();-->
<!--        if (this.dataset) {-->
<!--            this.title = this.dataset!.title;-->
<!--            this.description = this.dataset!.description;-->
<!--        }-->
<!--    }-->

<!--    public cancel() {-->
<!--        this.$router.back();-->
<!--    }-->

<!--    public async submit() {-->
<!--        if (await this.$validator.validateAll()) {-->
<!--            const updatedDataset: IDatasetUpdate = {title: '', description: '', data: []};-->
<!--            if (this.title) {-->
<!--                updatedDataset.title = this.title;-->
<!--            }-->
<!--            if (this.description) {-->
<!--                updatedDataset.title = this.description;-->
<!--            }-->
<!--            if (this.data) {-->
<!--                updatedDataset.data = this.data;-->
<!--            }-->
<!--            await dispatchUpdateDataset(this.$store, {id: this.dataset!.id, dataset: updatedDataset});-->
<!--            this.$router.push('/main/datasets');-->

<!--        }-->
<!--    }-->

<!--    // public handleFilePondInit() {-->
<!--    //     console.log('FilePond has initialized');-->
<!--    //     // FilePond instance methods are available on `this.$refs.pond`-->
<!--    // }-->
<!--}-->
<!--</script>-->
