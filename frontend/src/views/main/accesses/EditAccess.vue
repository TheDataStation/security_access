<!--<template>-->
<!--    <v-container fluid>-->
<!--        <v-card class="ma-3 pa-3">-->
<!--            <v-card-title primary-title>-->
<!--                <div class="headline primary&#45;&#45;text">Create Query</div>-->
<!--            </v-card-title>-->
<!--            <v-card-text>-->
<!--                <template>-->
<!--                    <v-form-->
<!--                        ref="form"-->
<!--                        v-model="valid"-->
<!--                        lazy-validation-->
<!--                    >-->
<!--                        <v-textarea-->
<!--                            v-model="description"-->
<!--                            auto-grow-->
<!--                            box-->
<!--                            label="Description"-->
<!--                        ></v-textarea>-->
<!--                        <v-textarea-->
<!--                            v-model="payload"-->
<!--                            auto-grow-->
<!--                            box-->
<!--                            label="Payload"-->
<!--                        ></v-textarea>-->
<!--                        <v-select-->
<!--                            :items="queryTypes"-->
<!--                            box-->
<!--                            label="Query type"-->
<!--                        ></v-select>-->
<!--                        &lt;!&ndash;                        <div class="subheading secondary&#45;&#45;text text&#45;&#45;lighten-2">Files</div>&ndash;&gt;-->
<!--                        &lt;!&ndash;                        <v-divider></v-divider>&ndash;&gt;-->
<!--                        &lt;!&ndash;                        <p></p>&ndash;&gt;-->
<!--                        <file-pond-->
<!--                            ref="pond"-->
<!--                            :allow-multiple="true"-->
<!--                            accepted-file-types="image/jpeg, image/png"-->
<!--                            label-idle="Drop files here..."-->
<!--                            name="file"-->
<!--                            v-on:init="handleFilePondInit"-->
<!--                            v-on:processfile="handleFilePondUploadFile"-->
<!--                        />-->
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
<!--import {dispatchCreateDataset, dispatchCreateQuery, dispatchGetQueries} from '@/store/actions';-->
<!--import {IDatasetCreate, IQueryCreate, IQueryType} from '@/interfaces';-->

<!--// Import Vue FilePond-->
<!--import VueFilePond from 'vue-filepond';-->
<!--// Import FilePond styles-->
<!--import 'filepond/dist/filepond.min.css';-->
<!--import {setOptions} from 'filepond';-->
<!--import {api} from '@/api';-->
<!--import {readLastDataset, readToken} from '@/store/getters';-->
<!--import {store} from '@/store';-->


<!--const FilePond = VueFilePond();-->

<!--/* tslint:disable:no-bitwise */-->
<!--function hashCode(str: string) {-->
<!--    let hash = 0;-->
<!--    if (str.length === 0) {-->
<!--        return hash;-->
<!--    }-->
<!--    for (let i = 0; i < str.length; i++) {-->
<!--        const char = str.charCodeAt(i);-->
<!--        hash = ((hash << 5) - hash) + char;-->
<!--        hash = hash & hash; // Convert to 32bit integer-->
<!--    }-->
<!--    return hash.toString();-->
<!--}-->
<!--/* tslint:enable:no-bitwise */-->


<!--@Component({-->
<!--    components: {-->
<!--        FilePond,-->
<!--    },-->
<!--})-->
<!--export default class CreateQuery extends Vue {-->
<!--    public valid = true;-->
<!--    public loading = false;-->
<!--    public type: IQueryType = IQueryType.IOther;-->
<!--    public description?: string = '';-->
<!--    public fileIds: any[] = [];-->
<!--    public queryTypes = Object.keys(IQueryType).map((k) => IQueryType[k as any].toUpperCase());-->
<!--    public payload: string = '';-->
<!--    // json-->
<!--    private blindml = {-->
<!--        task: {-->
<!--            type: 'regression',-->
<!--            payload: {-->
<!--                y_col: 'energy_above_hull (meV/atom)',-->
<!--                drop_cols: [-->
<!--                    'formation_energy (eV/atom)',-->
<!--                    'Material Composition',-->
<!--                    'A site #1',-->
<!--                    'A site #2',-->
<!--                    'A site #3',-->
<!--                    'B site #1',-->
<!--                    'B site #2',-->
<!--                    'B site #3',-->
<!--                    'X site',-->
<!--                ],-->
<!--            },-->
<!--        },-->
<!--        dos: {-->
<!--            metric: 'accuracy',-->
<!--            range: [0.8, 1],-->
<!--        },-->
<!--        trust_constraints: {-->
<!--            freshness: 'last_week',-->
<!--            user: 'all_groups',-->
<!--        },-->
<!--    };-->

<!--    public handleFilePondInit() {-->
<!--        // FilePond instance methods are available on `this.$refs.pond`-->
<!--        // console.log(this.$refs.pond);-->
<!--    }-->

<!--    public handleFilePondUploadFile(err, file) {-->
<!--        this.fileIds.push(parseInt(file.serverId, 10));-->
<!--    }-->

<!--    public async mounted() {-->
<!--        setOptions({-->
<!--            server: {-->
<!--                url: api.uploadUrl,-->
<!--                ...api.authHeaders(readToken(store)),-->
<!--            },-->
<!--        });-->
<!--        await dispatchGetQueries(this.$store);-->

<!--        this.reset();-->
<!--    }-->

<!--    public reset() {-->
<!--        this.type = IQueryType.IOther;-->
<!--        this.description = '';-->
<!--        this.payload = JSON.stringify(this.blindml, null, 8);-->
<!--        this.loading = false;-->
<!--        this.$validator.reset();-->
<!--    }-->

<!--    public cancel() {-->
<!--        this.$router.back();-->
<!--    }-->

<!--    public async submit() {-->
<!--        if (await this.$validator.validateAll()) {-->
<!--            const createdQuery: IQueryCreate = {-->
<!--                description: this.description,-->
<!--                type: this.type,-->
<!--                payload: this.payload,-->
<!--            };-->
<!--            const createdDataset: IDatasetCreate = {-->
<!--                title: `query ${new Date().toJSON()}`,-->
<!--                description: `${hashCode(this.payload)}`,-->
<!--                file_ids: this.fileIds,-->
<!--            };-->
<!--            // TODO(max): on failure files don't get deleted server side-->
<!--            await dispatchCreateDataset(this.$store, createdDataset);-->
<!--            const dataset = readLastDataset(this.$store);-->
<!--            await dispatchCreateQuery(this.$store, {query: createdQuery, datasetId: dataset.id});-->
<!--            await this.$router.push('/main/queries');-->

<!--        }-->
<!--    }-->
<!--}-->
<!--</script>-->

