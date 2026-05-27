import { StoryViewScaffold } from "@/components/story/StoryViewScaffold";
import { getStoryView } from "@/lib/site";

export function BuildingView() {
  return <StoryViewScaffold view={getStoryView("building")} />;
}
