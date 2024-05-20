import {expect, vitest, test} from 'vitest';
import {Me} from '../../src/types/me.ts';

vitest.mock('react-i18next', () => ({
    useTranslation: () => ({t: (key: any) => key})
}));

test.todo("Header test")
