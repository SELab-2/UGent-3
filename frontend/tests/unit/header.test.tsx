import { vitest, test } from "vitest";

vitest.mock("react-i18next", () => ({
  useTranslation: () => ({ t: (key: any) => key }),
}));

test.todo("Header test");
