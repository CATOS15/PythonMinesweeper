import Vue, { VNode } from 'vue'
import  GlobalData  from "/models/globalData";

declare global {
  namespace JSX {
    // tslint:disable no-empty-interface
    interface Element extends VNode {}
    // tslint:disable no-empty-interface
    interface ElementClass extends Vue {}
    interface IntrinsicElements {
      [elem: string]: any;
    }
  }

  
  interface Vue {
      $globaldata: GlobalData;
  }
}


