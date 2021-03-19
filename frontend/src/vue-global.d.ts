import GlobalData from "./models/globalData";

declare module "vue/types/vue"{
    interface Vue{
        $globaldata:GlobalData;
    }
}