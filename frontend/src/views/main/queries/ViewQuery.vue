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
                    <prism-editor readonly v-model="payload" :highlight="highlighter" class="my-editor"
                                  line-numbers></prism-editor>

                    <!--                    <v-textarea-->
                    <!--                        v-model="payload"-->
                    <!--                        auto-grow-->
                    <!--                        box-->
                    <!--                        disabled-->
                    <!--                        label="Payload"-->
                    <!--                    ></v-textarea>-->
                    <p></p>
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
import { IQueryType } from '@/interfaces';
import { dispatchGetQueries } from '@/store/actions';
import { readOneQuery } from '@/store/getters';
import 'prismjs/components/prism-clike';
// import highlighting library (you can use any library you want just return html string)
// noinspection ES6UnusedImports
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-json';
import 'prismjs/themes/prism-tomorrow.css';
import { PrismEditor } from 'vue-prism-editor'; // import syntax highlighting styles
// import Prism Editor
import 'vue-prism-editor/dist/prismeditor.min.css'; // import the styles somewhere
import { Component, Vue } from 'vue-property-decorator';

@Component({
  components: {
    PrismEditor,
  },
})
export default class ViewQuery extends Vue {
  public description?: string = '';
  public type: IQueryType = IQueryType.IOther;
  public fileIds: any[] = [];
  public payload: string = '';

  public async mounted() {
    await dispatchGetQueries(this.$store);
    const query = readOneQuery(this.$store)(
      +this.$router.currentRoute.params.id,
    );
    this.payload = JSON.stringify(query!.payload, null, 4);
    this.description = query!.description;
    this.type = query!.type!;
  }

  public cancel() {
    this.$router.back();
  }

  public highlighter(code) {
    return highlight(code, languages.js); // languages.<insert language> to return html with markup
  }
}
</script>

<style>
/* required class */
.my-editor {
    /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
    background: #2d2d2d;
    color: #ccc;

    /* you must provide font-family font-size line-height. Example: */
    font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
    font-size: 14px;
    line-height: 1.5;
    padding: 5px;
}

/* optional class for removing the outline */
.prism-editor__textarea:focus {
    outline: none;
}
</style>